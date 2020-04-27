/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Application} app
 */

const addComment = `
    mutation comment($id: ID!, $body: String!) {
      addComment(input: {subjectId: $id, body: $body}) {
        clientMutationId
      }
    }
  `

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

      // console.log(blameResponse['repositoryOwner']['repository']['object']['blame']['ranges'][0]['commit'])
      const params = context.repo({ path: filesChanged[i] })
      const contents = await context.github.repos.getContents(params)

      var spawn = require('child_process').spawn,
      py    = spawn('python', ['test.py']),
      data = blameResponse,
      dataString = '';

      py.stdout.on('data', function(data){
        dataString += data.toString();
      });

      /*Once the stream is done (on 'end') we want to simply log the received data to the console.*/
      py.stdout.on('end', function(){
        const JSONDataString = JSON.parse(dataString)
        const params = context.repo({ commit_sha: context.payload.head_commit.id, body: JSONDataString, path: filesChanged[i], position: 1, line: 6 })
        context.github.repos.createCommitComment(params)
        console.log('Commit Comment: ', JSONDataString);
      });

      py.stdin.write(contents['data']['download_url']);
      py.stdin.write('\n')
      py.stdin.write(JSON.stringify(data));
      py.stdin.end();
    }
  })
}
