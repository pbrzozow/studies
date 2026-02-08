using GradeSystem.Interfaces;
using GradeSystem.Models;
using GradeSystem.Services;

class Program
{
    static void Main()
    {
        var gradeService = new GradeService();
        IDataService<Grade> gradeDataService = gradeService;
        ICsvHandler<Grade> gradeCsvHandler = gradeService;
        var reportService = new ReportService();

        var users = new List<User>
        {
            new Teacher(1, "teacher", "123", "Jan", "Nowak"),
            new Student(2, "student", "123", "Anna", "Kowalska", "S123")
        };

        while (true)
        {
            Console.Write("Login: ");
            string login = Console.ReadLine();
            Console.Write("Hasło: ");
            string password = Console.ReadLine();

            var user = users.FirstOrDefault(u => u.Login == login && u.Password == password);
            if (user == null)
            {
                Console.WriteLine("Błędne dane logowania\n");
                continue;
            }

            bool logged = true;
            while (logged)
            {
                user.ShowMenu();
                string choice = Console.ReadLine();

                try
                {
                    if (user is Teacher)
                        HandleTeacherMenu(choice, gradeDataService, gradeCsvHandler, reportService, ref logged);
                    else if (user is Student student)
                        HandleStudentMenu(choice, gradeDataService, student, ref logged);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Błąd: " + ex.Message);
                }
            }
        }
    }

    private static void HandleTeacherMenu(string c, IDataService<Grade> service, ICsvHandler<Grade> csvHandler, ReportService report, ref bool run)
    {
        if (c == "1")
        {
            Console.Write("ID studenta: ");
            int sid = int.Parse(Console.ReadLine());
            Console.Write("Przedmiot: ");
            string sub = Console.ReadLine();
            Console.Write("Ocena: ");
            int val = int.Parse(Console.ReadLine());
            service.Add(new Grade(sid, sub, val));
        }
        else if (c == "2")
        {
            Console.Write("ID oceny: ");
            int id = int.Parse(Console.ReadLine());
            Console.Write("Nowa ocena: ");
            int val = int.Parse(Console.ReadLine());
            var g = service.GetAll().First(x => x.Id == id);
            g.ChangeValue(val);
            service.Update(g);
        }
        else if (c == "3")
        {
            Console.Write("ID oceny: ");
            service.Delete(int.Parse(Console.ReadLine()));
        }
        else if (c == "4")
        {
            Console.Write("ID studenta: ");
            int sid = int.Parse(Console.ReadLine());
            Console.WriteLine("Średnia: " + report.CalculateAverage(service.GetAll(), sid));
        }
        else if (c == "5") csvHandler.Export("grades.csv");
        else if (c == "6") csvHandler.Import("grades.csv");
        else if (c == "0") run = false;
    }

    private static void HandleStudentMenu(string c, IDataService<Grade> service, Student student, ref bool run)
    {
        if (c == "1")
        {
            foreach (var g in service.GetAll().Where(x => x.StudentId == student.Id))
                Console.WriteLine($"{g.Subject}: {g.Value}");
        }
        else if (c == "0") run = false;
    }
}
