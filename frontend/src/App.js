import React, { Component } from 'react'
import './App.css'

class App extends Component {
    constructor(props) {
      super(props)
      this.state = {term: '', results: []}
  
      this.handleSubmit = this.handleSubmit.bind(this)
    }

    handleSubmit(event) {
      event.preventDefault()
      fetch('http://127.0.0.1:5002/search', {
        method: 'POST',
        body: JSON.stringify({
          term: this.state.term
        })
      })
      .then(response => response.json() )
      .then(results => {
        this.setState({results:results})
      })
      .catch(error => console.warn(error))
    }
  
    render() {
      const messages = this.state.results.map(function(r, i){
        return (
          <div key={i}>{r.username}: {r.content}</div>
        )
      })
      return (
        <form onSubmit={this.handleSubmit}>
          <label>
            Search Logs:
          </label>
          <p>
            <input type="text" name="term" value={this.state.term} onChange={e => this.setState({term: e.target.value})} />
          </p>
          <p><input type="submit" value="Submit" /></p>
          { messages }
        </form>
      )
    }
  }

export default App