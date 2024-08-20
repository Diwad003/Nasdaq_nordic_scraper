#include <nasdaq_handler.h>

int main(void)
{
    FILE* fp;
    fp = fopen("output.txt", "r");
    
    int amountOfCompanies = 0;
    Company** companyList = ExtractDataFromFile(fp, &amountOfCompanies);
    
}