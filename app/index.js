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
  app.on('push', async context => {
    const commits = context.payload.commits
    var filesChanged = []
    var i
    for (i = 0; i < commits.length; i++) {
      filesChanged = filesChanged.concat(commits[i]['modified'])
    }

    for (i = 0; i < filesChanged.length; i++) {
      const blameResponse = await context.github.graphql(blame, {
        login: context.payload.repository.owner.name,
        name: context.payload.repository.name,
        path: filesChanged[i]
      })

      const params = context.repo({ path: filesChanged[i] })
      const contents = await context.github.repos.getContents(params)

      let pyshell = new PythonShell('funnel.py');
      data = blameResponse,
      dataString = '';

      pyshell.send(contents['data']['download_url']);
      pyshell.send(JSON.stringify(data));

      pyshell.on('message', function (data) {
        dataString += data.toString();
        dataString = JSON.parse(dataString)
      });

      pyshell.end(function (err,code,signal) {
        if (err) throw err;
        const params = context.repo({ commit_sha: context.payload.head_commit.id, body: dataString['6'], path: filesChanged[i], position: 1, line: 1 })
        context.github.repos.createCommitComment(params)
        console.log('The exit code was: ' + code);
        console.log('The exit signal was: ' + signal);
        console.log('finished');
      });
    }
  })
}
