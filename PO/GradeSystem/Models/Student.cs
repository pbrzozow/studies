namespace GradeSystem.Models;

public sealed class Student : Person
{
    public string IndexNumber { get; }

    public Student(int id, string login, string password, string firstName, string lastName, string index)
        : base(id, login, password, firstName, lastName)
    {
        IndexNumber = index;
    }

    public override void ShowMenu()
    {
        Console.WriteLine("1. Wyświetl moje oceny");
        Console.WriteLine("0. Wyloguj");
    }
}