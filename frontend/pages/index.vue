<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row key justify="center">
      <v-col
        cols="4"
        style="text-align:center"
      >
        <div
          class="pa-10"
        >
          <logo />
        </div>
        <v-text-field
          v-model="queryString"
          outlined
          rounded
          single-lined
          prepend-inner-icon="mdi-magnify"
          @keydown="searchOnEnter"
        />
        <v-btn
          outlined
          @click="search"
        >
          search
        </v-btn>
      </v-col>
    </v-row>
    <v-row />
  </v-container>
</template>

<script>
import Logo from '~/components/Logo.vue'

export default {
  components: {
    Logo
  },
  data () {
    return {
      queryString: ''
    }
  },
  methods: {
    searchOnEnter (e) {
      if (e.key === 'Enter') {
        this.search()
      }
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
