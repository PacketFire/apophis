import React from 'react'
import { BrowserRouter as Router, Route, Link } from "react-router-dom"
import Search from './Search'
import Permissions from './Permissions'

const Navigation = () => (
  <Router>
    <nav>
      <ul>
        <li>
          <Link to="/">Index</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li>
          <Link to="/dashboard">Dashboard</Link>
        </li>
      </ul>

      <hr />

      <Route exact path="/" component={Index} />
      <Route path="/about" component={About} />
      <Route path="/dashboard" component={Dashboard} />
    </nav>
  </Router>
);

const Index = () => (
  <section>
    <h2>Index</h2>
  </section>
);

const About = () => (
  <section>
    <h2>About</h2>
  </section>
);

const Dashboard = ({match}) => (
  <section>
    <h2>Dashboard</h2>
    <ul>
      <li>
        <Link to={`${match.url}/search`}>Search</Link>
      </li>
      <li>
        <Link to={`${match.url}/permissions`}>Permissions</Link>
      </li>
    </ul>

    <Route path={`${match.url}/search`} component={Search} />
    <Route path={`${match.url}/permissions`} component={Permissions} />

  </section>
);

export default Navigation
