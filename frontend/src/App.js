import React, { Component } from 'react';
import './App.css';

class App extends Component {
    constructor(props) {
      super(props);
      this.state = {term: '', results: ''};
  
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
      event.preventDefault()
      fetch('http://localhost:5002/search', {
        method: 'POST',
        body: JSON.stringify({
          term: this.state.term
        })
      })
      .then(response => response.json())
      .then(results => this.setState({results: results}))
      .catch(error => console.error('Error:', error));
    }
  
    render() {
      const { data } = this.state;
      return (
        <form onSubmit={this.handleSubmit}>
          <label>
            Search Logs:
            <input type="text" name="term" value={this.state.term} onChange={e => this.setState({term: e.target.value})} />
          </label>
          <p><input type="submit" value="Submit" /></p>
          <p>{ data }</p>
        </form>
      );
    }
  }

export default App;
