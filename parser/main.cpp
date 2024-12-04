#include "requests.hpp"
#include "db_usage.hpp"

int main()
{
    database::open_db();

    requests::getRequest("s9603567", "s9603770", "2024-12-4");

    return 0;
}
