import React, { Component } from 'react'

class Navigation extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <nav>
              <ul>
                <li><a href="#">Index</a></li>
                <li><a href="#">About</a></li>
              </ul>
            </nav>
        )
    }
}

export default Navigation
