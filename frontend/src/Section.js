import React, { Component } from 'react'
import Search from './Search'

function Section(props) {
    return (
        <section>
            <h2>Dashboard</h2>
            <article>
                 <Search />
            </article>
        </section>
    )
}

export default Section