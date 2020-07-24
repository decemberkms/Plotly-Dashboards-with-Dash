# bin limit calculator
# Function
# by MIN

import numpy as np
import pandas as pd
import math

def _bin_limit_calculator(df_all, lambda_dict):
    new_limit_list = []

    # calculatiomn with optimal lambda
    for key,value in lambda_dict.items():
        if value[0] >= -2 and value[0] < 0:  # negative lambda

            if len(df_all[df_all[key] != 0][key][177:]) < 50:
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                #print('@@@@@@@@  ' + key + '  @@@@@@@@@')
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                # a = parameter list
                a = df_all[df_all[key] != 0][key][-50:]
                boxcox_proper_with_lamda = np.power(a*0.01, round(value[0], 3))
                #boxcox_proper_with_lamda = stats.boxcox(a, round(value[0], 3))
                #plt.hist(boxcox_proper_with_lamda, bins = 25,  color = 'blue')
                #####################
                q_1 = np.percentile(boxcox_proper_with_lamda,25)
                q_3 = np.percentile(boxcox_proper_with_lamda,75)
                iqr = q_3-q_1
                outlier_low = q_1 - 1.5*iqr
                outlier_high = q_3 + 1.5*iqr
                #print("outlier low =", outlier_low)
                #print("outlier high =", outlier_high)
                #####################
                #####################
                outliers = []
                for i in boxcox_proper_with_lamda:
                    if i < outlier_low or i > outlier_high:
                        outliers.append(i)
                a_exp_outlier =[item for item in boxcox_proper_with_lamda if item not in outliers] # list comprehension for outliers
                #a_exp_outlier = np.setdiff1d(boxcox_proper_with_lamda, outliers)
                #print(outliers)
                ##print(boxcox_proper_with_lamda)
                ####################
                ####################
                mean_boxcox = np.mean(a_exp_outlier)
                std_boxcox = np.std(a_exp_outlier,ddof = 1)
                ####################
                bin_limit_in_box_cox = mean_boxcox - 3*std_boxcox
                #print(len(boxcox_proper_with_lamda))

                #print("Mean: ", mean_boxcox)
                #print("Std: ", std_boxcox)
                #print("Lambda: ", value[0])
                inverse_trans_bin_limit = math.pow(abs(bin_limit_in_box_cox), 1/value[0])
                #print('*************************************' )
                #print("Bin limit of {}".format(key), str(round(inverse_trans_bin_limit * 100, 5)) + '%')
                #print('*************************************' )
                ##print(boxcox_proper_with_lamda)
                new_limit_list.append(round(inverse_trans_bin_limit * 100, 5))

            elif len(df_all[df_all[key] != 0][key][177:]) >= 50:
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                #print('@@@@@@@@  ' + key + '  @@@@@@@@@')
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                # a = parameter list
                a = df_all[df_all[key] != 0][key][177:]
                boxcox_proper_with_lamda = np.power(a*0.01,round(value[0], 3))
                #boxcox_proper_with_lamda = stats.boxcox(a, round(value[0], 3))
                #plt.hist(boxcox_proper_with_lamda, bins = 25,  color = 'blue');
                #####################
                q_1 = np.percentile(boxcox_proper_with_lamda,25)
                q_3 = np.percentile(boxcox_proper_with_lamda,75)
                iqr = q_3-q_1
                outlier_low = q_1 - 1.5*iqr
                outlier_high = q_3 + 1.5*iqr
                #print("outlier low =", outlier_low)
                #print("outlier high =", outlier_high)
                #####################
                #####################
                outliers = []
                for i in boxcox_proper_with_lamda:
                    if i < outlier_low or i > outlier_high:
                        outliers.append(i)
                a_exp_outlier =[item for item in boxcox_proper_with_lamda if item not in outliers] # list comprehension for outliers
                #a_exp_outlier = np.setdiff1d(boxcox_proper_with_lamda, outliers)
                #print(outliers)
                ##print(boxcox_proper_with_lamda)
                ####################
                ####################
                mean_boxcox = np.mean(a_exp_outlier)
                std_boxcox = np.std(a_exp_outlier,ddof = 1)
                ####################
                bin_limit_in_box_cox = mean_boxcox - 3*std_boxcox
                #print(len(boxcox_proper_with_lamda))

                #print("Mean: ", mean_boxcox)
                #print("Std: ", std_boxcox)
                #print("Lambda: ", value[0])
                inverse_trans_bin_limit = math.pow(bin_limit_in_box_cox, 1/value[0])
                #print('*************************************' )
                #print("Bin limit of {}".format(key), str(round(inverse_trans_bin_limit * 100, 5)) + '%')
                #print('*************************************' )
                ##print(boxcox_proper_with_lamda)
                new_limit_list.append(round(inverse_trans_bin_limit * 100, 5))

        elif value[0] == 0:  # lambda =0

            if len(df_all[df_all[key] != 0][key][177:]) < 50:
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                #print('@@@@@@@@  ' + key + '  @@@@@@@@@')
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                # a = parameter list
                a = df_all[df_all[key] != 0][key][-50:]
                boxcox_proper_with_lamda = np.log(a*0.01)
                #boxcox_proper_with_lamda = stats.boxcox(a, round(value[0], 3))
                #plt.hist(boxcox_proper_with_lamda, bins = 25,  color = 'blue');
                #####################
                q_1 = np.percentile(boxcox_proper_with_lamda,25)
                q_3 = np.percentile(boxcox_proper_with_lamda,75)
                iqr = q_3-q_1
                outlier_low = q_1 - 1.5*iqr
                outlier_high = q_3 + 1.5*iqr
                #print("outlier low =", outlier_low)
                #print("outlier high =", outlier_high)
                #####################
                outliers = []
                for i in boxcox_proper_with_lamda:
                    if i < outlier_low or i > outlier_high:
                        outliers.append(i)
                a_exp_outlier =[item for item in boxcox_proper_with_lamda if item not in outliers] # list comprehension for outliers
                #a_exp_outlier = np.setdiff1d(boxcox_proper_with_lamda, outliers)
                #print(outliers)
                ##print(boxcox_proper_with_lamda)
                ####################
                ####################
                mean_boxcox = np.mean(a_exp_outlier)
                std_boxcox = np.std(a_exp_outlier,ddof = 1)
                ####################
                bin_limit_in_box_cox = mean_boxcox + 3*std_boxcox
                #print(len(boxcox_proper_with_lamda))

                #print("Mean: ", mean_boxcox)
                #print("Std: ", std_boxcox)
                #print("Lambda: ", value[0])
                inverse_trans_bin_limit = math.exp(bin_limit_in_box_cox)
                #print('*************************************' )
                #print("Bin limit of {}".format(key), str(round(inverse_trans_bin_limit * 100, 5)) + '%')
                #print('*************************************' )
                ##print(boxcox_proper_with_lamda)
                new_limit_list.append(round(inverse_trans_bin_limit * 100, 5))

            elif len(df_all[df_all[key] != 0][key][177:]) >= 50:
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                #print('@@@@@@@@  ' + key + '  @@@@@@@@@')
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                # a = parameter list
                a = df_all[df_all[key] != 0][key][177:]
                boxcox_proper_with_lamda = np.log(a*0.01)
                #boxcox_proper_with_lamda = stats.boxcox(a, round(value[0], 3))
                #plt.hist(boxcox_proper_with_lamda, bins = 25,  color = 'blue');
                #####################
                q_1 = np.percentile(boxcox_proper_with_lamda,25)
                q_3 = np.percentile(boxcox_proper_with_lamda,75)
                iqr = q_3-q_1
                outlier_low = q_1 - 1.5*iqr
                outlier_high = q_3 + 1.5*iqr
                #print("outlier low =", outlier_low)
                #print("outlier high =", outlier_high)
                #####################
                outliers = []
                for i in boxcox_proper_with_lamda:
                    if i < outlier_low or i > outlier_high:
                        outliers.append(i)
                a_exp_outlier =[item for item in boxcox_proper_with_lamda if item not in outliers] # list comprehension for outliers
                #a_exp_outlier = np.setdiff1d(boxcox_proper_with_lamda, outliers)
                #print(outliers)
                ##print(boxcox_proper_with_lamda)
                ####################
                ####################
                mean_boxcox = np.mean(a_exp_outlier)
                std_boxcox = np.std(a_exp_outlier,ddof = 1)
                ####################
                bin_limit_in_box_cox = mean_boxcox + 3*std_boxcox
                #print(len(boxcox_proper_with_lamda))

                #print("Mean: ", mean_boxcox)
                #print("Std: ", std_boxcox)
                #print("Lambda: ", value[0])
                inverse_trans_bin_limit = math.exp(bin_limit_in_box_cox)
                #print('*************************************' )
                #print("Bin limit of {}".format(key), str(round(inverse_trans_bin_limit * 100, 5)) + '%')
                #print('*************************************' )
                ##print(boxcox_proper_with_lamda)
                new_limit_list.append(round(inverse_trans_bin_limit * 100, 5))

        else:  # positive lambda

            if len(df_all[df_all[key] != 0][key][177:]) < 50:
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                #print('@@@@@@@@  ' + key + '  @@@@@@@@@')
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                # a = parameter list
                a = df_all[df_all[key] != 0][key][-50:]
                boxcox_proper_with_lamda = np.power(a*0.01,round(value[0], 3))
                #boxcox_proper_with_lamda = stats.boxcox(a, round(value[0], 3))
                #plt.hist(boxcox_proper_with_lamda, bins = 25,  color = 'blue');
                #####################
                q_1 = np.percentile(boxcox_proper_with_lamda,25)
                q_3 = np.percentile(boxcox_proper_with_lamda,75)
                iqr = q_3-q_1
                outlier_low = q_1 - 1.5*iqr
                outlier_high = q_3 + 1.5*iqr
                #print("outlier low =", outlier_low)
                #print("outlier high =", outlier_high)
                #####################
                outliers = []
                for i in boxcox_proper_with_lamda:
                    if i < outlier_low or i > outlier_high:
                        outliers.append(i)
                a_exp_outlier =[item for item in boxcox_proper_with_lamda if item not in outliers] # list comprehension for outliers
                #a_exp_outlier = np.setdiff1d(boxcox_proper_with_lamda, outliers)
                #print(outliers)
                ##print(boxcox_proper_with_lamda)
                ####################
                ####################
                mean_boxcox = np.mean(a_exp_outlier)
                std_boxcox = np.std(a_exp_outlier,ddof = 1)
                ####################
                bin_limit_in_box_cox = mean_boxcox + 3*std_boxcox
                #print(len(boxcox_proper_with_lamda))

                #print("Mean: ", mean_boxcox)
                #print("Std: ", std_boxcox)
                #print("Lambda: ", value[0])
                inverse_trans_bin_limit = math.pow(bin_limit_in_box_cox, 1/value[0])
                #print('*************************************' )
                #print("Bin limit of {}".format(key), str(round(inverse_trans_bin_limit * 100, 5)) + '%')
                #print('*************************************' )
                ##print(boxcox_proper_with_lamda)
                new_limit_list.append(round(inverse_trans_bin_limit * 100, 5))

            elif len(df_all[df_all[key] != 0][key][177:]) >= 50:
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                #print('@@@@@@@@  ' + key + '  @@@@@@@@@')
                #print('@@@@@@@@@@@@@@@@@@@@@@@@@@')
                # a = parameter list
                a = df_all[df_all[key] != 0][key][177:]
                boxcox_proper_with_lamda = np.power(a*0.01,round(value[0], 3))
                #boxcox_proper_with_lamda = stats.boxcox(a, round(value[0], 3))
                #plt.hist(boxcox_proper_with_lamda, bins = 25,  color = 'blue');
                #####################
                q_1 = np.percentile(boxcox_proper_with_lamda,25)
                q_3 = np.percentile(boxcox_proper_with_lamda,75)
                iqr = q_3-q_1
                outlier_low = q_1 - 1.5*iqr
                outlier_high = q_3 + 1.5*iqr
                #print("outlier low =", outlier_low)
                #print("outlier high =", outlier_high)
                #####################
                outliers = []
                for i in boxcox_proper_with_lamda:
                    if i < outlier_low or i > outlier_high:
                        outliers.append(i)
                a_exp_outlier =[item for item in boxcox_proper_with_lamda if item not in outliers] # list comprehension for outliers
                #a_exp_outlier = np.setdiff1d(boxcox_proper_with_lamda, outliers)
                #print(outliers)
                ##print(boxcox_proper_with_lamda)
                ####################
                ####################
                mean_boxcox = np.mean(a_exp_outlier)
                std_boxcox = np.std(a_exp_outlier,ddof = 1)
                ####################
                bin_limit_in_box_cox = mean_boxcox + 3*std_boxcox
                #print(len(boxcox_proper_with_lamda))

                #print("Mean: ", mean_boxcox)
                #print("Std: ", std_boxcox)
                #print("Lambda: ", value[0])
                inverse_trans_bin_limit = math.pow(bin_limit_in_box_cox, 1/value[0])
                #print('*************************************' )
                #print("Bin limit of {}".format(key), str(round(inverse_trans_bin_limit * 100, 5)) + '%')
                #print('*************************************' )
                ##print(boxcox_proper_with_lamda)
                new_limit_list.append(round(inverse_trans_bin_limit * 100, 5))

    return new_limit_list # return new limits
