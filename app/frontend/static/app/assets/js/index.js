import '../styles/main.css'
import '../styles/auth.css'
import '../styles/dashboard.css'
import '../styles/dropdown.css'
import '../styles/practice.css'
import '../styles/profile.css'
import '../styles/tools.css'
require('animate.css')

const bulma = require('bulma');
import { toast } from 'bulma-toast';


function hi() {
    console.log("I am damn called!");
}

export {
    hi,
    toast
}

