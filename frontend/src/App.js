import React, { Component } from 'react';
import './App.css';

class App extends Component {
    constructor(props) {
      super(props);
      this.state = {username: '', password: ''};
  
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
      event.preventDefault()
      fetch('http://localhost:5002/login', {
        method: 'POST',
        body: JSON.stringify({
          username: this.state.username, 
          password: this.state.password
        })
      }).then(function(responseBody){
        console.log(responseBody.username);
      });
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          <p>
          <label>
            Username:
            <input type="text" name="username" value={this.state.username} onChange={e => this.setState({username: e.target.value})} />
          </label>
          </p>
          <p>
          <label>
            Password:
            <input type="password" name="password" value={this.state.password} onChange={e => this.setState({password: e.target.value})} />
          </label>
          </p>
          <p><input type="submit" value="Login" /></p>
        </form>
      );
    }
  }

export default App;
