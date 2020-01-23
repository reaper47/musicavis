require('./all_css.js')

import { toast } from 'bulma-toast'
import Main from './main.js'

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

export { toast, Main }
