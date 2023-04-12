import './sass/app.scss'
import * as bootstrap from 'bootstrap';
window.bootstrap = bootstrap;

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'
/* import specific icons */
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
/* add icons to the library */
library.add(faUserSecret)