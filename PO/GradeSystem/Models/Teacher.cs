namespace GradeSystem.Models;

public sealed class Teacher : Person
{
    public Teacher(int id, string login, string password, string firstName, string lastName)
        : base(id, login, password, firstName, lastName) { }

    public override void ShowMenu()
    {
        Console.WriteLine("1. Dodaj ocenę");
        Console.WriteLine("2. Edytuj ocenę");
        Console.WriteLine("3. Usuń ocenę");
        Console.WriteLine("4. Raport – średnia studenta");
        Console.WriteLine("5. Eksport CSV");
        Console.WriteLine("6. Import CSV");
        Console.WriteLine("0. Wyloguj");
    }
}