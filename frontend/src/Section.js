import React, { Component } from 'react'
import Search from './Search'

class Section extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <section>
                <h2>Dashboard</h2>
                <article>
                    <Search />
                </article>
            </section>
 
        )
    }
}

export default Section