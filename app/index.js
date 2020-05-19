/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Application} app
 */

let {PythonShell} = require('python-shell')

const blame = `
query blame($login: String!, $name: String!, $path: String!){
  repositoryOwner(login: $login) {
    repository(name: $name) {
      object(expression: "master") {
        ... on Commit {
          blame(path: $path) {
            ranges {
              startingLine
              endingLine
              age
              commit {
                oid
                authoredDate
                author {
                  name
                }
              }
            }
          }
        }
      }
    }
  }
}
`


module.exports = app => {
  app.on(['pull_request.opened', 'pull_request.edited'], async context => {
    const params = context.repo({pull_number: context.payload.pull_request.number})
    const filesChanged = await context.github.pulls.listFiles(params)

    var i
    for (i = 0; i < filesChanged['data'].length; i++) {
      const blameResponse = await context.github.graphql(blame, {
        login: context.payload.repository.owner.login,
        name: context.payload.repository.name,
        path: filesChanged['data'][i]['filename']
      })

      let pyshell = new PythonShell('funnel.py');
      data = blameResponse,
      dataString = '';

      pyshell.send(context.payload.repository.name);
      pyshell.send(filesChanged['data'][i]['filename']);
      pyshell.send(filesChanged['data'][i]['blob_url']);
      pyshell.send(filesChanged['data'][i]['raw_url']);
      pyshell.send(JSON.stringify(data));

      pyshell.on('message', function (data) {
        dataString += data.toString();
        dataString = JSON.parse(dataString)
      });
      app.log(dataString)
      pyshell.end(function (err,code,signal) {
        if (err) throw err;
        const params = context.repo({ pull_number:
          context.payload.pull_request.number,
          commit_id: filesChanged['data'][i]['sha'],
          path: filesChanged['data'][i]['filename'], start_line: 1,
          start_side: 'LEFT', line: 3, side: 'RIGHT', body: dataString })
        context.github.pulls.createComment(params)
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
      });
    }
  })
}
