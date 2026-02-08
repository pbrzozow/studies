namespace GradeSystem.Models;

public abstract class Person : User
{
    public string FirstName { get; }
    public string LastName { get; }

    protected Person(int id, string login, string password, string firstName, string lastName)
        : base(id, login, password)
    {
        FirstName = firstName;
        LastName = lastName;
    }
}