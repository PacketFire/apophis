import React, { Component } from 'react'
import { BrowserRouter as Route, Link } from "react-router-dom"


class Permissions extends Component {
    constructor(props) {
        super(props)
        this.state = {results: []}
        this.handleClick = this.handleClick.bind(this)
    }

    componentDidMount() {
      fetch('http://127.0.0.1:5002/permissions')
      .then(response => response.json() )
      .then(results => {
        this.setState({results:results})
      })
      .catch(error => console.warn(error));
    }

    handleClick(username) {
      fetch('http://127.0.0.1:5002/permissions/' + username, {
        method: 'DELETE'
      })
      .catch(error => console.warn(error))
    }

    render() {
        const perms = this.state.results.map(function(r, i){
            return (
                  <tr>
                    <td>{r.id}</td>
                    <td>{r.username}</td>
                    <td>{r.level}</td>
                    <td>
                      <input type="checkbox" onClick={e => this.handleClick(r.username)} />
                    </td>
                  </tr>
            )
        })
        return (
              <article>
                <h3>Permissions</h3>
                  <ul>
                    <li>
                      <Link to="/add">Add</Link>
                    </li>
                  </ul>
                  <table>
                    <tr>
                      <th>ID</th>
                      <th>Username</th>
                      <th>Level</th>
                      <th>Delete</th>
                      <th></th>
                    </tr>
                    { perms }
                  </table>
                  <Route path="/add" component={AddPerm} />
              </article>
        )
    }
}

class AddPerm extends Component {
    constructor(props) {
      super(props)
      this.state = {username: '', level: ''}
  
      this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(event) {
      event.preventDefault()
      fetch('http://127.0.0.1:5002/permissions', {
        method: 'POST',
        body: JSON.stringify({
          username: this.state.username,
          level: this.state.level
        })
      })
      .catch(error => console.warn(error))
    }
  
    render() {
      return (
        <article>
          <form onSubmit={this.handleSubmit}>
            <label>
              Add Permissions
            </label>
            <p>
              <label>
                Username:<input type="text" name="username" value={this.state.username} onChange={e => this.setState({username: e.target.value})} />
              </label>
            </p>
            <p>
              <label>
                Level:<input type="text" name="level" value={this.state.level} onChange={e => this.setState({level: e.target.value})} />
              </label>
            </p>
            <p><input type="submit" value="Submit" /></p>
          </form>
        </article>
      )
    }
  }

export default Permissions