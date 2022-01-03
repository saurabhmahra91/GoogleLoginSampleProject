import React from 'react'
import { Link } from 'react-router-dom';

export default function Nav() {
  return (
    <div className="nav">
      <h2>
        GoogleLoginSampleApp
      </h2>
      <ul>
        <li>
          <Link to="/"> Homepage</Link>
        </li>
        <li>
          <Link to="/login"> Login</Link>
        </li>
        <li>
          <Link to="/time"> Time</Link>
        </li>
      </ul>
    </div>
  )
}
