require('./all_css.js')

import { toast } from 'bulma-toast'
import Main from './main.js'
import { makeSearchableDropDown, SearchableDropdown } from './dropdown.js'
import { Timer, Metronome } from './tools.js'
import pushNewInstrument from './profile.js'
import Practice from './practice.js'

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}


export {
    toast,
    Main,
    makeSearchableDropDown, SearchableDropdown,
    Timer, Metronome,
    pushNewInstrument,
    Practice
}

