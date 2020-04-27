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
    // console.log('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
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
      // console.log("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
      // console.log(blameResponse['repositoryOwner']['repository']['object']['blame']['ranges'][0]['commit'])
    }
  })
}
