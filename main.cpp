#include <iostream>
#include <string>
#include <climits>
#include <sstream>
#include <fstream>

#define KST 50

class Visitor
{
private:
    std::string Fio;
    std::string Address;
    int Year;

public:
    Visitor() {}
    Visitor(const std::string &fio, const std::string &address, int year)
        : Fio(fio), Address(address), Year(year) {}

    std::string GetFio() const { return Fio; }
    int GetYear() const { return Year; }
};

class Library
{
private:
    Visitor visitors[KST];
    int visitorCount;

public:
    Library() : visitorCount(0) {}

    void Run()
    {
        std::ofstream outputFile("output.txt");
        if (!outputFile)
        {
            std::cout << "Помилка відкриття файлу output.txt.\n";
            return;
        }

        GetVisitorData(); // Виклик методу для зчитування даних відвідувачів з input.txt

        std::ostringstream outputBuffer; // Буфер для виводу

        outputBuffer << "Середній вік: ";
        MiddleAge(outputBuffer);

        outputBuffer << "Найстарший відвідувач: ";
        TheOldestPerson(outputBuffer);

        outputBuffer << "Наймолодший відвідувач: ";
        TheYoungestPerson(outputBuffer);

        outputFile << outputBuffer.str(); // Запис у файл
        outputFile.close();
        std::cout << "Дані записані у файл 'output.txt'.\n";
    }

private:
    void GetVisitorData()
    {
        std::ifstream inputFile("input.txt");
        if (!inputFile)
        {
            std::cout << "Помилка відкриття файлу input.txt.\n";
            return;
        }

        std::string line;
        while (std::getline(inputFile, line))
        {
            std::istringstream iss(line);
            std::string fio, address, yearStr;

            if (std::getline(iss, fio, ';') && std::getline(iss, address, ';') && std::getline(iss, yearStr, ';'))
            {
                int year = std::stoi(yearStr);

                visitors[visitorCount] = Visitor(fio, address, year);
                visitorCount++;

                if (visitorCount >= KST)
                    break;
            }
        }
        inputFile.close();
    }

    void MiddleAge(std::ostream &out)
    {
        int ageSum = 0;
        for (int i = 0; i < visitorCount; i++)
            ageSum += 2024 - visitors[i].GetYear();
        int averageAge = ageSum / visitorCount;
        out << averageAge << " років\n";
    }

    void TheOldestPerson(std::ostream &out)
    {
        int minYear = INT_MAX;
        for (int i = 0; i < visitorCount; i++)
        {
            int year = visitors[i].GetYear();
            if (year < minYear)
                minYear = year;
        }
        for (int i = 0; i < visitorCount; i++)
        {
            if (visitors[i].GetYear() == minYear)
            {
                out << visitors[i].GetFio() << " (" << minYear << " рік)\n";
                break;
            }
        }
    }

    void TheYoungestPerson(std::ostream &out)
    {
        int maxYear = 0;
        for (int i = 0; i < visitorCount; i++)
        {
            int year = visitors[i].GetYear();
            if (year > maxYear)
                maxYear = year;
        }
        for (int i = 0; i < visitorCount; i++)
        {
            if (visitors[i].GetYear() == maxYear)
            {
                out << visitors[i].GetFio() << " (" << maxYear << " рік)\n";
                break;
            }
        }
    }
};

int main()
{
    system("chcp 65001"); 
    Library library;
    library.Run();
    return 0;
}
