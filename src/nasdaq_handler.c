#include <nasdaq_handler.h>
#include <string_library.h>

/**
 * Parses company data from a file and returns a dynamically allocated array of `Company` pointers.
 *
 * @param fp A pointer to the `FILE` object to read from. The file should be open and formatted with
 *           company records enclosed between `<tr>` tags.
 * @param companyListMaxIndex A pointer to an integer that keeps track of the number of companies 
 *                            added to the list. This value is updated to reflect the total number 
 *                            of records processed.
 * @return A pointer to an array of `Company*`, where each element is a dynamically allocated 
 *         `Company` structure containing the extracted data. The caller is responsible for freeing
 *         this memory.
 *
 * The function reads through the file line by line, extracting data for each company enclosed
 * between `<tr>` tags. It expects specific data formatting and copies attributes like company symbol,
 * currency, ISIN, sector, and ICB from the file into dynamically allocated `Company` structures.
 *
 * Note:
 * - Ensure `SIZE_OF_COMPANY_LIST` is defined to provide initial allocation size for `companyList`.
 * - The function does not handle memory allocation failures or malformed data.
 * - The caller must free the allocated memory for each `Company` structure and the array of pointers.
 */
Company** ExtractDataFromFile(FILE* fp, int* companyListMaxIndex)
{
    Company** companyList = malloc(SIZE_OF_COMPANY_LIST * sizeof(Company*));
    char line[256];
    char output[256];

    while (fgets(line, sizeof(line), fp))
    {
        if(strcmp(line, "<tr>\n") == 0)
        {
            fgets(line, sizeof(line), fp);
            fgets(line, sizeof(line), fp);//Skip two lines

            companyList[*companyListMaxIndex] = malloc(sizeof(Company));

            ExtractBetweenValue(line, '>', '<', output);
            companyList[*companyListMaxIndex]->companySymbol = malloc(strlen(output)+1);
            strcpy(companyList[*companyListMaxIndex]->companySymbol, output);

            fgets(line, sizeof(line), fp);
            ExtractBetweenValue(line, '>', '<', output);
            companyList[*companyListMaxIndex]->currency = malloc(strlen(output)+1);
            strcpy(companyList[*companyListMaxIndex]->currency, output);

            fgets(line, sizeof(line), fp);
            ExtractBetweenValue(line, '>', '<', output);
            companyList[*companyListMaxIndex]->ISIN = malloc(strlen(output)+1);
            strcpy(companyList[*companyListMaxIndex]->ISIN, output);

            fgets(line, sizeof(line), fp);
            ExtractBetweenValue(line, '>', '<', output);
            companyList[*companyListMaxIndex]->sector = malloc(strlen(output)+1);
            strcpy(companyList[*companyListMaxIndex]->sector, output);

            fgets(line, sizeof(line), fp);
            ExtractBetweenValue(line, '>', '<', output);
            companyList[*companyListMaxIndex]->ICB = malloc(strlen(output)+1);
            strcpy(companyList[*companyListMaxIndex]->ICB, output);
            
            (*companyListMaxIndex)++;
        }
    }
    fclose(fp);

    return companyList;
}