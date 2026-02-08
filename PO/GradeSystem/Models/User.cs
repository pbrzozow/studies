namespace GradeSystem.Models;

public abstract class User
{
    public int Id { get; }
    public string Login { get; }
    public string Password { get; }

    protected User(int id, string login, string password)
    {
        Id = id;
        Login = login;
        Password = password;
    }

    public abstract void ShowMenu();
}