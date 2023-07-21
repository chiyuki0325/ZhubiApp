/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import themes from './themes.js'

// Composables
import { createVuetify } from 'vuetify'
import { md3 } from 'vuetify/blueprints'
import * as components from 'vuetify/lib/components/index'
import * as directives from 'vuetify/lib/directives/index'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: 'BlueMountainsLight',
    themes
  },
  components,
  directives,
  blueprint: md3,
  icons: {
    defaultSet: 'mdi'
  }
})
