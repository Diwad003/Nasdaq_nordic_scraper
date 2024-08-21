#include <nasdaq_handler.h>

int main(void)
{
    FILE* fp;
    Company** companyList;
    int amountOfCompanies = 0;


    fp = fopen("output.txt", "r");
    companyList = ExtractDataFromFile(fp, &amountOfCompanies);


    char* pythonCommand = malloc(1024);
    sprintf(pythonCommand, "python3 ./CompanyInfoScraper.py https://www.nasdaqomxnordic.com/shares/microsite?Instrument=%s temp.txt", companyList[0]->ISIN);
    printf("Command: %s\n", pythonCommand);
    int result = system(pythonCommand);
    if (result == -1) 
    {
        perror("system");
    } 
    else 
    {
        printf("Command executed with return code: %d\n", result);
    }
    free(pythonCommand);;

    return 0;   
}