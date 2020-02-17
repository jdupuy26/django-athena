import React, { Component } from 'react';
import { PageSection, Title, Page } from '@patternfly/react-core';


class Dashboard extends Component<{}, {data: any, loaded: boolean, placeholder: string}> {

  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("/api/repos/")
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


export { Dashboard };
