import React from 'react';
import { useEffect, useState, useLayoutEffect } from 'react';
import axios from "axios";

export default function Time() {
    const [time, setTime] = useState("Loading............")
    useEffect(() => {
        axios.get("http://localhost:5000/time").then((response)=>{setTime(response.data.time)});
    })
    return (
        <div className='time'>
            {time}
        </div>
    )
}
