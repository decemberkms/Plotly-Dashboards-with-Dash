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

ui <- basicPage(
    titlePanel(sprintf("MPE Limits aktualisiert am %s", "22/07/2020")),
    DT::dataTableOutput("mytable")
)

server <- function(input, output,session) {
    
    setwd("W://Technology//NY-FMMT614-7-55//FT")

    df_zero <- reactiveFileReader(5000, session, filePath ="FT_statistic//NY_bin_statistics.xlsx",readFunc = read_excel)
    df_limit_zero <- reactiveFileReader(5000, session, filePath ="FT_statistic//MPE_limit_update_limit.xlsx", readFunc = read_excel)
    df_comment <- reactiveFileReader(5000, session, filePath ="FT_statistic//NY_bin_comment.xlsx", readFunc = read_excel)
    
    output$mytable = DT::renderDataTable({
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
        print(df0_1)
        
        #---------------- add dummy columns to the front
        df_limit <- cbind(Charge = 0, Testdatum = 0, df_limit)
        print(df_limit)
        df0_1 <- rbind(df_limit, df0_1)
        df0_1$Charge[1] <- 'MPE Limits'
        
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
                backgroundColor = styleEqual(c('MPE Limits'), c('#a2de96'))
            ) %>% formatStyle(
                'Comment_L',
                target = 'row',
                backgroundColor = styleEqual(1, c('#d63447'))
            )
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
