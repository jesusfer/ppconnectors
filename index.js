const express = require("express")
const path = require("path")

const app = express()
const port = 8000

app.use(
  "/",
  express.static(path.join(__dirname, "docs/"), {
    index: "index.html",
  })
)

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
})
