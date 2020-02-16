import React, { Component } from 'react';
import { PageSection, Title, Page } from '@patternfly/react-core';


class Dashboard extends Component<{}> {

  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    // todo figure out how to get relative paths working
    fetch("http://localhost:8000/api/repos/")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!"};
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <PageSection>
        <Title size="lg">Athena ++ Codes and Branches</Title>
        <ul>
          {this.state.data.map(repo => {
            return (
              <li key={repo.name}>
                {repo.name} - {repo.url}
              </li>
            );
          })}
        </ul>
      </PageSection>
    )
  }
}


// const Dashboard: React.FunctionComponent<{}> = () => (
//     <PageSection>
//       <Title size="lg">Athena ++ Codes and Branches</Title>
//     </PageSection>
//   )

export { Dashboard };
