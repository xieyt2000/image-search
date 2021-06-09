<template>
  <div>
    <div
      class="single-line"
      style="margin-top:1em;"
    >
      Page Title
    </div>
    <div
      class="single-line"
      style="color:grey;font-size:0.8em;"
    >
      root url
    </div>
  </div>
</template>
<script>
export default {
  name: 'ImageUrls'
}
</script>
<style>
.single-line {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.single-line:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
