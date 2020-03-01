class RefCountry(object):

    # https://en.wikipedia.org/wiki/List_of_NATO_country_codes + BZH (29 rpz)
    countryList = ['ATG', 'AFG', 'DZA', 'AZE', 'ALB', 'ARM', 'AND', 'AGO', 'ARG', 'AUS', 'AUT', 'BHR', 'BRB', 'BWA',
                   'BZH', 'BEL', 'BHS', 'BGD', 'BLZ', 'BIH', 'BOL', 'MMR', 'BEN', 'BLR', 'SLB', 'BRA', 'BTN', 'BGR',
                   'BRN', 'BDI', 'CAN', 'KHM', 'TCD', 'LKA', 'COG', 'COD', 'CHN', 'CHL', 'CMR', 'COM', 'COL', 'CRI',
                   'CAF', 'CUB', 'CPV', 'CYP', 'CZE', 'DNK', 'DJI', 'DMA', 'DOM', 'ECU', 'EGY', 'GNQ', 'EST', 'ERI',
                   'SLV', 'ETH', 'FIN', 'FJI', 'FRA', 'FYR', 'GMB', 'GAB', 'DEU', 'GEO', 'GHA', 'GRD', 'GRC', 'GTM',
                   'GIN', 'GUY', 'HTI', 'HND', 'HRV', 'HUN', 'ISL', 'IDN', 'IRL', 'IND', 'IRN', 'ISR', 'ITA', 'CIV',
                   'IRQ', 'JPN', 'JAM', 'JOR', 'KEN', 'KGZ', 'PRK', 'KIR', 'KOR', 'KWT', 'KAZ', 'LAO', 'LBN', 'LVA',
                   'LTU', 'LBR', 'LIE', 'LSO', 'LUX', 'LBY', 'MDG', 'FSM', 'MDA', 'MNG', 'MWI', 'MLI', 'MCO', 'MAR',
                   'MUS', 'MRT', 'MNP', 'MHL', 'MLT', 'ODM', 'MDV', 'MEX', 'MYS', 'MOZ', 'NER', 'VUT', 'NGA', 'NLD',
                   'NOR', 'NPL', 'NRU', 'SUR', 'NIC', 'NZL', 'PRY', 'PER', 'PAK', 'POL', 'PAN', 'PRT', 'PNG', 'GNB',
                   'PLW', 'QAT', 'ROU', 'PHL', 'PRI', 'RUS', 'RWA', 'SAU', 'KNA', 'SYC', 'ZAF', 'SEN', 'SVN', 'SVK',
                   'SLE', 'SMR', 'SGP', 'SOM', 'ESP', 'LCA', 'SDN', 'SWE', 'SYR', 'CHE', 'ARE', 'TTO', 'TLS', 'THA',
                   'TJK', 'TON', 'TGO', 'STP', 'TUN', 'TUV', 'TUR', 'TWN', 'TKM', 'TZN', 'UGA', 'GBR', 'UKR', 'USA',
                   'BFA', 'URY', 'UZB', 'VCT', 'VEN', 'VNM', 'VAT', 'NAM', 'WSM', 'SWZ', 'YEM', 'ZMB', 'ZWE', 'SRB']
