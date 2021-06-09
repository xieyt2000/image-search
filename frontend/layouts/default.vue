<template>
  <v-app>
    <v-app-bar
      v-if="$route.path==='/search/'"
      color="#ffffff"
    >
      <img
        src="/vuetify-logo.svg"
        style="height:100%;cursor:pointer"
        alt="go-index"
        @click="$router.push({path:'/'})"
      >
      <div style="height:100%; width:30%">
        <v-text-field
          v-model="queryString"
          class="mx-4"
          outlined
          rounded
          single-lined
          prepend-inner-icon="mdi-magnify"
          @keydown="searchOnEnter"
        />
      </div>
      <v-dialog
        v-model="filterDialog"
        width="25%"
      >
        <template #activator="{ on }">
          <v-btn
            icon
            v-on="on"
          >
            <v-icon>mdi-filter-outline</v-icon>
          </v-btn>
        </template>

        <v-card>
          <v-card-title primary-title>
            Filter
          </v-card-title>

          <v-container>
            <v-row>
              <v-col>
                <v-select
                  v-model="size"
                  class="ma-2"
                  :items="Object.values(SIZE)"
                  label="Image size"
                  outlined
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-select
                  v-model="colorType"
                  class="ma-2"
                  :items="Object.values(COLOR_TYPE)"
                  label="Color"
                  outlined
                />
              </v-col>
            </v-row>
            <v-row v-if="colorType===COLOR_TYPE.PICK">
              <v-spacer />
              <v-col>
                <v-color-picker
                  v-model="color"
                  class="ma-2"
                  hide-mode-switch
                />
              </v-col>
              <v-spacer />
            </v-row>
          </v-container>

          <v-divider />
          <v-card-actions>
            <v-spacer />
            <v-btn
              color="primary"
              @click="filterDialog = false;filterSearch()"
            >
              SEARCH
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-spacer />
    </v-app-bar>
    <v-content style="width:100%">
      <nuxt />
    </v-content>
  </v-app>
</template>

<script>
import { COLOR_TYPE, SIZE } from 'static/constant'

export default {
  components: {},
  data () {
    return {
      queryString: '',
      filterDialog: false,
      size: SIZE.ANY,
      color: '',
      colorType: COLOR_TYPE.ANY
    }
  },
  watch: {
    '$route.path' () {
      if (this.$route.path === '/search/') {
        this.init()
      }
    },
    '$route.query' () {
      if (this.$route.path === '/search/') {
        this.init()
      }
    }
  },
  created () {
    this.SIZE = SIZE
    this.COLOR_TYPE = COLOR_TYPE
  },
  mounted () {
    if (this.$route.path === '/search/') {
      this.init()
    }
  },
  methods: {
    searchOnEnter (e) {
      if (e.key === 'Enter') {
        this.search()
      }
    },
    init () {
      this.queryString = this.$route.query.query ? this.$route.query.query : ''
      this.size = this.$route.query.size ? this.$route.query.size : SIZE.ANY
      this.color = this.$route.query.color ? this.$route.query.color : '#000000'
      this.colorType = this.$route.query.color ? COLOR_TYPE.PICK : COLOR_TYPE.ANY
    },
    filterSearch () {
      const query = {
        query: this.queryString,
        size: this.size,
        colorType: this.colorType,
        color: this.color
      }
      if (query.size === SIZE.ANY) {
        delete query.size
      }
      if (query.colorType === COLOR_TYPE.ANY) {
        delete query.color
      }
      delete query.colorType
      this.$router.push({
        path: '/search/',
        query
      })
    },
    search () {
      this.$router.push({
        path: '/search/',
        query: {
          query: this.queryString
        }
      })
    }
  }
}
</script>
