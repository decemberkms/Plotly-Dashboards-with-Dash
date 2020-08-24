# remove all the variables in the work space
rm(list= ls())


#--------------------- call packages or install if there isn't any
#install.packages("readxl")
library("readxl")
#install.packages("dplyr")
library("dplyr")
#install.packages("openxlsx")
library("openxlsx")
#install.packages("reshape2")
# library("reshape2")
#install.packages("tidyr")
library("tidyr")

#--------------------- check the current working directory
getwd()

#--------------------- set the working directory where the statistics for NY is
setwd("W://Technology//NY-FMMT614-7-55//FT")

#--------------------- read the excel file (NY) as df
df <- read_excel("FT_statistic//NY_bin_statistics.xlsx")  # >  package readxl
df_comment <- read_excel("FT_statistic//NY_bin_comment.xlsx")

#--------------------- change to categorical variables- lot, sub lot, bin name and bin number
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
  summarise(100*count/sum(count)) # > package dplyr

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
df1_1 <- spread(data=df1, bin_number, percentage) # > package tidyr
df2_1 <- spread(data=df2, bin_number, percentage) # > package tidyr
df3_1 <- spread(data=df3, bin_number, percentage) # > package tidyr

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

#--------------------- inserting a column for comment in the report 
library("tibble")  # for inserting a column in a dataframe
dummy3 <- rep(NA, nrow(df0_1))
df0_1 <- add_column(df0_1, dummy3, .after = "VBESAT") # > package tibble

#---------------------  remove old dataframes
rm(df0,df1,df2,df3,df1_1,df2_1,df3_1, dummy,dummy3)


#--------------------- edit RTH due to the format of excel file
df0_1$RTH <- df0_1$RTH * 0.01

#--------------------- change dateformat
df0_1$date <- strftime(df0_1$date, format="%m/%d/%Y")


#--------------------- Load existing file
wb = loadWorkbook("MPE Report//MPE_FMMT614-7-55_Vorlage_3 - Copy.xlsx") # > package openxlsx

#--------------------- Put the data back into the workbook
YY <- format(Sys.time(), "%G")
WW <- as.character(as.numeric(format(Sys.time(), "%V")) -1)
weekcode <- paste('WW',WW,' ', YY, sep='')
writeData(wb, sheet=1, weekcode, xy=c("B",2), colNames= FALSE)
writeData(wb, sheet=1, x=df0_1, xy= c("A", 14), colNames = FALSE) # > package openxlsx

#---------------------  save excel file
saveWorkbook(wb, paste("MPE Report//372S00032_FMMT614-7-55_MPE_", YY, "_WW", WW, '.xlsx', sep=""), overwrite=TRUE) # > package openxlsx

df0_1[!complete.cases(df0_1),]

?complete.cases()





df0_1 <- cbind(Charge = 0, Testdatum = 0, df0_1)
df0_1
year = "2008"
mnth = "1"
day = "31"
url = sprintf("https:.../KBOS/%s/%s/%s/DailyHistory.html", year, mnth, day)
url
Sys.time


df_comment
