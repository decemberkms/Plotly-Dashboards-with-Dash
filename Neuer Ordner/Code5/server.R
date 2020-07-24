library(RODBC)
library(data.table)
library(DT)
library(shiny)
# install.packages("lettercase")
library("lettercase")

shinyServer(function(input, output, session){
  
  output$text1 <- renderText({
    #paste("<font size=\"14\">AZQ Zusammenfassung am<font/>",format(Sys.time(), '%d. %B %Y'))
    paste("<h3>AZQ Zusammenfassung am",format(Sys.time(), '%d. %B %Y'))
  })
  
  output$table <- DT::renderDataTable(DT::datatable({
    con  <- odbcConnect("ZNGFinalTest")
    p <- sqlQuery(con, "SELECT * FROM report.vw_azq")
    close(con);
    if(nrow(p) == 0)return(NULL)
    p$cause <- paste(p$class,":<br>",p$cause, sep="")
    p$edit_user <- gsub("^.*?EU\\\\","",p$edit_user)
    name <- strsplit(p$edit_user,"_")
    name <- lapply(name, function(x){str_ucfirst(x)})
    name <- lapply(name, function(x){paste(x[1],x[2])})
    p$edit_user <- name
    p$owner_status <- paste(p$edit_user, "<br>", p$edit_date, sep="")
    
    p$create_user <- gsub("^.*?EU\\\\","",p$create_user)
    name <- strsplit(p$create_user,"_")
    name <- lapply(name, function(x){str_ucfirst(x)})
    name <- lapply(name, function(x){paste(x[1],x[2])})
    p$create_user <- name
    p$owner_start <- paste(p$create_user, "<br>", p$create_date, sep="")
    df <- data.frame(p$product, p$lot, p$wafers, p$affected, p$bonding_goods, p$cause, p$owner_start,p$comment, p$owner_status)
    colnames(df) <- c("Typ", "Lot","Wafer", "Betroffen","Gesamt", "Ausfallursache", "Startdatum","Status", "Statusdatum")
    #df <- as.data.frame(lapply(df, function(x){gsub("\r?\n|\r", "<br>", x)}))
    #df$Wafer <- lapply(df$Wafer,function(x){gsub(", ", "<br>", x)})
    myFun <- function(x, minLen = 3, onlyUnique = TRUE) {
      a <- if (isTRUE(onlyUnique)) unique(x) else x
      paste(a[nchar(a) > minLen], collapse = "<br>")
    }
    i <- sapply(df, is.factor)
    df[i] <- lapply(df[i], as.character)
    df$Wafer <- vapply(strsplit(df$Wafer, ", "), myFun, character(1L))
    df$Betroffen <- round(as.numeric(df$Betroffen), digits=-3)
    df$Betroffen <- paste(df$Betroffen/1000,"k", sep="")
    df$Gesamt <- round(as.numeric(df$Gesamt), digits=-3)
    df$Gesamt <- paste(df$Gesamt/1000,"k", sep="")
    df$Betroffen <- paste(df$Betroffen," / ",df$Gesamt,sep="")
    df <- subset(df, select = -c(Gesamt))
    unique(df)
    #Hier temporär neue Lose eintragen!
    #new.df <- data.frame(Typ = "ZXMN3B01F" , Lot = "389072", Wafer="9W32BOTHY.4", Betroffen = "8k / 193k", Ausfallursache = "Qualität:<br>IDSS", Status = "Erhöhter Blown on Test<br> Gurtausfälle sind bewertet<br> Freigabe HHa")
    #df <- rbind(df,new.df)
    df
  },
  class = "compact cell-border stripe",
  rownames = FALSE,
  escape = FALSE,
  options = list(
    paging = FALSE,
    info=FALSE,
    dom = 't',
    language = list(search = 'Filter:'),
    initComplete = JS(
      "function(settings, json) {",
      "$(this.api().table().header()).css({'background-color': '#C1C1C1', 'color': '#000'});",
      "}"
    )
  )
  ))
  
  output$text2 <- renderText({
    con  <- odbcConnect("ZNGFinalTest")
    p <- sqlQuery(con, "SELECT * FROM report.vw_azq")
    close(con);
    if(nrow(p) == 0)return("Liste leer!")
    paste("<h5>Zuletzt aktualisiert:",p$edit_date[rev(order(p$edit_date))][1])
  })
})