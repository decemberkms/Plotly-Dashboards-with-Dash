library(DT)
shinyUI(fluidPage(
  # title = (paste("AZQ: ",format(Sys.time(), '%d. %B %Y'))),
  title = ("AZQ"),
  tags$head(tags$link(rel = "shortcut icon", href = "favicon.ico")),
  fluidRow(
    column(12, align="center",
           # h4(paste("AZQ Zusammenfassung am",format(Sys.time(), '%d. %B %Y')), align = "center"),
           htmlOutput("text1"),
           DT::dataTableOutput("table"),
           #h5("Monitor:", a("FZT/ZX5T955", href="955_kw7.xlsx", target="_blank")),
           htmlOutput("text2")
    )		
  )
))