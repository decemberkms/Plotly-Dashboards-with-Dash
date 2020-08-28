# remove all the variables in the work space
rm(list= ls())

library(DT)
library(shiny)
#install.packages("readxl")
library(readxl)
#install.packages("dplyr")
library("dplyr")
#install.packages("openxlsx")
library("openxlsx")
#install.packages("reshape2")
library("reshape2")
#install.packages("tidyr")
library("tidyr")
# install.packages("zoo")

options(shiny.port = 8100, shiny.host='0.0.0.0')

# Define UI for random distribution app ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("MPE limits"),
  
 
  # Output: Tabset w/ plot, summary, and table ----
  tabsetPanel(type = "tabs",
              tabPanel("NY MPE", DT::dataTableOutput("fmmt614")),
              tabPanel("1008 MPE", DT::dataTableOutput("ZX1008")),
              tabPanel("Table3", DT::dataTableOutput("mytable"))
  )

)



server <- function(input, output,session) {
  
  setwd("W://Technology//NY-FMMT614-7-55//FT")
  
  # data load for FMMT 614
  df_zero <- reactiveFileReader(5000, session, filePath ="FT_statistic//MPE FMMT614-7-55//NY_bin_statistics.xlsx",readFunc = read_excel)
  df_limit_zero <- reactiveFileReader(5000, session, filePath ="FT_statistic//MPE FMMT614-7-55//MPE_limit_update.xlsx", readFunc = read_excel)
  df_comment <- reactiveFileReader(5000, session, filePath ="FT_statistic//MPE FMMT614-7-55//NY_bin_comment.xlsx", readFunc = read_excel)
  
  # data load for 1008
  df1008_zero <- reactiveFileReader(5000, session, filePath ="FT_statistic//MPE ZTXC1008//1008_bin_statistics.xlsx",readFunc = read_excel)
  df1008_limit_zero <- reactiveFileReader(5000, session, filePath ="FT_statistic//MPE ZTXC1008//1008_MPE_limit_update.xlsx", readFunc = read_excel)
  df1008_comment <- reactiveFileReader(5000, session, filePath ="FT_statistic//MPE ZTXC1008//1008_bin_comment.xlsx", readFunc = read_excel)
  
  # ------------------------------------------------------------------ FMMT614 table
  output$fmmt614 = DT::renderDataTable({
    ##################### Data generation######################
    #--------------------- change to categorical variables- lot, sub lot, bin name and bin number
    df <- df_zero()
    df_limit <- df_limit_zero()
    df_comment <- df_comment()
    as.data.frame(df_comment)
    
    df$lot <- factor(df$lot)
    df$sub_lot <- factor(df$sub_lot)
    df$bin_name <- factor(df$bin_name)
    df$bin_number <- factor(df$bin_number)
    
    
    #-------------------- data filtering
    df <- df[df$bin_name != "Leer" & df$bin_name != "Kelvin",]
    df$lot <- paste(df$lot, "_", df$sub_lot, sep="")
    
    #-------------------- remove meaningless columns
    df$Spalte1 <- NULL
    df$Spalte2 <- NULL
    df$sub_lot <- NULL
    
    #--------------------- group by lot and sublot
    df$percentage <- df %>%    # %>% is like a pipe 
      group_by(lot) %>% 
      summarise(100*count/sum(count))
    
    #-------------------- column bind a dateframe from the old one
    df0 <- cbind(df[c("lot", "bin_name", "bin_number","date")], df$percentage %>% .$`100 * count/sum(count)`)
    
    #-------------------- name columns 
    colnames(df0) <- c("lot", "bin_name", "bin_number", "date", "percentage")
    
    #------------------- drop bin number
    df0$bin_name <- NULL
    
    #--------------------------- divide df0 into three part
    df1 = df0[1:33,]   # 11 test bins
    df2 = df0[34:585,]    # 12 test bins
    df3 = df0[586:nrow(df0),]    # 14 test bins
    
    # pivot the dataframes 
    df1_1 <- spread(data=df1, bin_number, percentage)
    df2_1 <- spread(data=df2, bin_number, percentage)
    df3_1 <- spread(data=df3, bin_number, percentage)
    
    #------------------------  edit df1_1 
    dummy <- rep(NA,3)  # create dummy column for RTh
    df1_1 <- cbind(df1_1, dummy) # add the column to df1_1
    colnames(df1_1) <- c("lot","date","FMMT614", "Grenzwert", "Totalausfall", "Blown on Test", 
                         "Offen", "Kurzschluss", "ICBO", "ICES", "IEBO", "VCESAT",
                         "VBESAT", "RTH") # change the column names
    
    #------------------------  edit df2_1 
    colnames(df2_1) <- c("lot","date","FMMT614", "Grenzwert", "Totalausfall", "Blown on Test", 
                         "Offen", "Kurzschluss", "ICBO", "ICES", "IEBO", "VCESAT",
                         "VBESAT", "RTH") # change the column names
    
    #------------------------  edit df3_1 
    df3_1$"1" <- df3_1$"1" + df3_1$"2" + df3_1$"3"
    
    df3_1$"2" <- NULL
    df3_1$"3" <- NULL  # delete two columns
    
    colnames(df3_1) <- c("lot","date","FMMT614", "Grenzwert", "Totalausfall", "Blown on Test", 
                         "Offen", "Kurzschluss", "ICBO", "ICES", "IEBO", "VCESAT", 
                         "VBESAT", "RTH") # change the column names
    
    #---------------------- add up df1_1, df2_1 and df3_1
    df0_1 <- rbind(df1_1,df2_1, df3_1)
    
    #---------------------- remove GW, TA and blown on test
    df0_1$Grenzwert <- NULL
    df0_1$Totalausfall <- NULL
    df0_1$`Blown on Test` <- NULL
    
    # #--------------------- inserting a column for comment in the report 
    # library("tibble")  # for inserting a column in a dataframe
    # dummy3 <- rep(NA, nrow(df0_1))
    # df0_1 <- add_column(df0_1, dummy3, .after = "VBESAT")
    
    #---------------------  remove old dataframes
    rm(df0,df1,df2,df3,df1_1,df2_1,df3_1,dummy)
    
    # df0_1[!complete.cases(df0_1),]
    
    # -------------------- fill missing values in RTH
    df0_1$RTH[1] = mean(df0_1$RTH[complete.cases(df0_1$RTH)])
    df0_1$RTH[2] = mean(df0_1$RTH[complete.cases(df0_1$RTH)])
    df0_1$RTH[3] = mean(df0_1$RTH[complete.cases(df0_1$RTH)])
    
    #-------------------- change time format and round values
    df0_1$date <- strftime(df0_1$date, format="%d/%m/%Y")
    df0_1 <- df0_1[-c(188,189,190,191),]
    df0_1[c("FMMT614", "Offen", "Kurzschluss", 
            "ICBO", "ICES", "IEBO", "VCESAT", 
            "VBESAT", "RTH")] <- round(df0_1[c("FMMT614", "Offen", 
                                               "Kurzschluss", "ICBO", "ICES", 
                                               "IEBO", "VCESAT", "VBESAT", 
                                               "RTH")], 3)
    
    #---------------- set column names
    colnames(df0_1) <- c("Charge", "Testdatum", "FMMT614", "Offen", "Kurzschluss", 
                         "ICBO", "ICES", "IEBO", "VCESAT", 
                         "VBESAT", "RTH")
    
    
    # ---------------- reverse data and divide quarterly 
    rownames(df0_1) <- NULL
    
    ## ------------ combine two columns for comments
    df0_1 <- merge(df0_1, df_comment, by="Charge")
    
    df0_1 <- df0_1[235:nrow(df0_1),]
    df0_1 <- df0_1[seq(dim(df0_1)[1],1),] # reverse data
    
    
    #---------------- add dummy columns to the front
    df_limit <- cbind(Charge = 0, Testdatum = 0, df_limit)
    
    df0_1 <- rbind(df_limit, df0_1)
    df0_1$Charge[1] <- 'MPE Limits'
    df0_1$Testdatum[1] <- 'upgedatet am 22/07/20'
    
    ###################### Data generation done ######################  
    
    datatable(df0_1)
    datatable(df0_1) %>% formatStyle(
      'FMMT614',
      backgroundColor = styleInterval(c(df_limit$FMMT614[1])-0.001, c('#d63447', 'white'))
    ) %>% formatStyle(
      'Offen',
      backgroundColor = styleInterval(c(df_limit$Offen[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'Kurzschluss',
      backgroundColor = styleInterval(c(df_limit$Kurzschluss[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'ICBO',
      backgroundColor = styleInterval(c(df_limit$ICBO[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'ICES',
      backgroundColor = styleInterval(c(df_limit$ICES[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'IEBO',
      backgroundColor = styleInterval(c(df_limit$IEBO[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'VCESAT',
      backgroundColor = styleInterval(c(df_limit$VCESAT[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'VBESAT',
      backgroundColor = styleInterval(c(df_limit$VBESAT[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'RTH',
      backgroundColor = styleInterval(c(df_limit$RTH[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'Charge',
      backgroundColor = styleEqual(c('MPE Limits'), c('#93b5e1'))
    ) %>% formatStyle(
      'Testdatum',
      backgroundColor = styleEqual(c('upgedatet am 22/07/20'), c('#93b5e1'))
    ) %>% formatStyle(
      'label',
      target = 'row',
      backgroundColor = styleEqual(2, c('#d63447'))  # not delivered / blocked
    ) %>% formatStyle(
      'label',
      target = 'row',
      backgroundColor = styleEqual(3, c('blue'))
    ) %>% formatStyle(
      'label',
      target = 'row',
      backgroundColor = styleEqual(1, c('#91d18b')) # delivered
    )
  })
  
  # ------------------------------------------------------1008 table
  output$ZX1008 = DT::renderDataTable({
    ##################### Data generation######################
    #--------------------- change to categorical variables- lot, sub lot, bin name and bin number
    df1008 <- df1008_zero()
    df1008_limit <- df1008_limit_zero()
    df1008_comment <- df1008_comment()
    as.data.frame(df1008_comment)
    
    df1008$lot <- factor(df1008$lot)
    df1008$sub_lot <- factor(df1008$sub_lot)
    df1008$bin_name <- factor(df1008$bin_name)
    df1008$bin_number <- factor(df1008$bin_number)
    
    
    #-------------------- data filtering
    df1008 <- df1008[df1008$bin_name != "Leer" & df1008$bin_name != "Kelvin",]
    df1008$lot <- paste(df1008$lot, "_", df1008$sub_lot, sep="")
    
    #-------------------- remove meaningless columns
    df1008$Spalte1 <- NULL
    df1008$Spalte2 <- NULL
    df1008$sub_lot <- NULL
    
    #--------------------- group by lot and sublot
    df1008$percentage <- df1008 %>%    # %>% is like a pipe 
      group_by(lot) %>% 
      summarise(100*count/sum(count))
    
    #-------------------- column bind a dateframe from the old one
    df1008_0 <- cbind(df1008[c("lot", "bin_name", "bin_number","date")], df1008$percentage %>% .$`100 * count/sum(count)`)
    
    #-------------------- name columns 
    colnames(df1008_0) <- c("lot", "bin_name", "bin_number", "date", "percentage")
    
    #------------------- drop bin number
    df1008_0$bin_name <- NULL
    
    # pivot the dataframes 
    df1008_1 <- spread(data=df1008_0, bin_number, percentage)
    
    # name columns
    colnames(df1008_1) <- c("Charge","Testdatum","ZXCT1008F", "CJ1-Leakage", "NoStart@2.5V", "Grenzwert", "Totalausfall", "Vin offen", "Load offen", "Iout offen") # change the column names
    
    # change time format 
    df1008_1$Testdatum <- strftime(df1008_1$Testdatum, format="%d/%m/%Y")
    
    # round
    df1008_1[c("ZXCT1008F", "CJ1-Leakage", "NoStart@2.5V", "Grenzwert", 
               "Totalausfall", "Vin offen", "Load offen", "Iout offen")] <- round(df1008_1[c("ZXCT1008F", "CJ1-Leakage", "NoStart@2.5V", "Grenzwert", 
                                                                                            "Totalausfall", "Vin offen", "Load offen", "Iout offen")], 3)
    # ------------ combine two columns for comments
    df1008_1 <- merge(df1008_1, df1008_comment, by="Charge")
    
    #---------------- add dummy columns to the front
    df1008_limit <- cbind(Charge = 0, Testdatum = 0, df1008_limit)
    
    df1008_1 <- df1008_1[seq(dim(df1008_1)[1],1),] # reverse data
    
    # bind limits 
    df1008_1 <- rbind(df1008_limit, df1008_1)
    df1008_1$Charge[1] <- 'MPE Limits'
    df1008_1$Testdatum[1] <- 'upgedatet am 26/08/20'
   
    ###################### Data generation done ######################  
    
    datatable(df1008_1)
    datatable(df1008_1) %>% formatStyle(
      'Charge',
      backgroundColor = styleEqual(c('MPE Limits'), c('#93b5e1'))
    ) %>% formatStyle(
      'Testdatum',
      backgroundColor = styleEqual(c('upgedatet am 26/08/20'), c('#93b5e1'))
    ) %>% formatStyle(
      'ZXCT1008F',
      backgroundColor = styleInterval(c(df1008_limit$ZXCT1008F[1])-0.001, c('#d63447', 'white'))
    ) %>% formatStyle(
      'CJ1-Leakage',
      backgroundColor = styleInterval(c(df1008_limit$'CJ1-Leakage'[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'NoStart@2.5V',
      backgroundColor = styleInterval(c(df1008_limit$'NoStart@2.5V'[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'Grenzwert',
      backgroundColor = styleInterval(c(df1008_limit$'Grenzwert'[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'Totalausfall',
      backgroundColor = styleInterval(c(df1008_limit$'Totalausfall'[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'Vin offen',
      backgroundColor = styleInterval(c(df1008_limit$'Vin offen'[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'Load offen',
      backgroundColor = styleInterval(c(df1008_limit$'Load offen'[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'Iout offen',
      backgroundColor = styleInterval(c(df1008_limit$'Iout offen'[1]), c('white', '#d63447'))
    ) %>% formatStyle(
      'label',
      target = 'row',
      backgroundColor = styleEqual(2, c('#d63447'))  # not delivered / blocked
    ) %>% formatStyle(
      'label',
      target = 'row',
      backgroundColor = styleEqual(3, c('blue'))
    ) %>% formatStyle(
      'label',
      target = 'row',
      backgroundColor = styleEqual(1, c('#91d18b')) # delivered
    )
  })
  
}

# Run the application 
shinyApp(ui = ui, server = server)