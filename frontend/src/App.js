import React, { Component } from 'react'
import Header from './Header'
import Navigation from './Navigation'
import Section from './Section'
import Footer from './Footer'

class App extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
                <Header />
                <Navigation />
                <Section />
                <Footer />
            </div>
        )
    }
}

export default App