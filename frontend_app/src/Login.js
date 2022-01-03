import { GoogleLogin } from 'react-google-login';
import { useState } from "react";
import axios from 'axios';
import { useSelector, useDispatch } from 'react-redux';

// const clientID = "1009912481477-rumk7lv3njmf7l3asoo7ee6808htfdtd.apps.googleusercontent.com";
// const clientSecret = "xVWz8LZBMnaXvr1YNXGtjvhH";

const clientID = "994801329917-keuej9ebn3tj301av05381mhnsdps7pm.apps.googleusercontent.com";

export default function Login() {
    const userJWT = useSelector((state)=>state.userJWT)
    const dispatch = useDispatch();
    // const [userJWT, setUserJWT] = useState(null)
    const [loginErrorMessage, setloginErrorMessage] = useState(null)
    // loginErrorMessage - cmmon variable for errors from backend form validation, google login error
    // const [loginErrorMessage, setloginErrorMessage] = useState(localStorage.getItem("loginErrorMessage") ? JSON.parse(localStorage.getItem("loginErrorMessage")) : null)

    const handleGoogleLoginSuccess = async (googleData) => {
        axios.post("http://localhost:5000/googleToken", { "googleData": googleData })
        .then((response) => {
            console.log(response.data)
            dispatch({type:"SET_USER_JWT", payload:response.data.token})
        })
        .catch((error)=>{
            setloginErrorMessage(error.message);
        })
    }
    
    const handleGoogleLogout = () => {
        dispatch({type:"UNSET_USER_JWT"})
    }
    const handleGoogleLoginFailure = (result) => {
        console.log("res", result.error);
        setloginErrorMessage(result.error);
    }

    return (
        <>
                {loginErrorMessage?<div>{loginErrorMessage}</div>:<div></div> }
                
                {
                    // If userJWT exists, do not render the login with google button, instead show logout button
                    userJWT
                        ? (<div>User LoggedIn Click here to Logout <button onClick={handleGoogleLogout}>LogOUT</button></div>)
                        :
                        (<GoogleLogin
                            clientId={clientID}
                            buttonText="Login with Google"
                            onSuccess={handleGoogleLoginSuccess}
                            onFailure={handleGoogleLoginFailure}
                            cookiePolicy={'single_host_origin'}
                        />)
                }


        </>
    )
}
