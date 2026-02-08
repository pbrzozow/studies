using GradeSystem.Interfaces;
using GradeSystem.Models;
using Microsoft.Data.Sqlite;

namespace GradeSystem.Services;

public sealed class GradeService : IDataService<Grade>, ICsvHandler<Grade>
{
    private const string DbFile = "grades.db";
    private readonly string _connectionString = "Data Source=" + DbFile;

    public GradeService()
    {
        InitializeDatabase();
    }

    private void InitializeDatabase()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        var cmd = connection.CreateCommand();
        cmd.CommandText =
            "CREATE TABLE IF NOT EXISTS Grades (" +
            "Id INTEGER PRIMARY KEY AUTOINCREMENT," +
            "StudentId INTEGER NOT NULL," +
            "Subject TEXT NOT NULL," +
            "Value INTEGER NOT NULL" +
            ");";
        cmd.ExecuteNonQuery();
    }

    public void Add(Grade grade)
    {
        using var con = new SqliteConnection(_connectionString);
        con.Open();

        var cmd = con.CreateCommand();
        cmd.CommandText = "INSERT INTO Grades(StudentId, Subject, Value) VALUES (@sid,@sub,@val)";
        cmd.Parameters.AddWithValue("@sid", grade.StudentId);
        cmd.Parameters.AddWithValue("@sub", grade.Subject);
        cmd.Parameters.AddWithValue("@val", grade.Value);
        cmd.ExecuteNonQuery();
    }

    public void Update(Grade grade)
    {
        using var con = new SqliteConnection(_connectionString);
        con.Open();

        var cmd = con.CreateCommand();
        cmd.CommandText = "UPDATE Grades SET Value=@val WHERE Id=@id";
        cmd.Parameters.AddWithValue("@val", grade.Value);
        cmd.Parameters.AddWithValue("@id", grade.Id);

        if (cmd.ExecuteNonQuery() == 0)
            throw new Exception("Nie znaleziono oceny");
    }

    public void Delete(int id)
    {
        using var con = new SqliteConnection(_connectionString);
        con.Open();

        var cmd = con.CreateCommand();
        cmd.CommandText = "DELETE FROM Grades WHERE Id=@id";
        cmd.Parameters.AddWithValue("@id", id);

        if (cmd.ExecuteNonQuery() == 0)
            throw new Exception("Nie znaleziono oceny");
    }

    public List<Grade> GetAll()
    {
        var list = new List<Grade>();

        using var con = new SqliteConnection(_connectionString);
        con.Open();

        var cmd = con.CreateCommand();
        cmd.CommandText = "SELECT Id, StudentId, Subject, Value FROM Grades";

        using var reader = cmd.ExecuteReader();
        while (reader.Read())
        {
            var g = new Grade(reader.GetInt32(1), reader.GetString(2), reader.GetInt32(3))
            {
                Id = reader.GetInt32(0)
            };
            list.Add(g);
        }

        return list;
    }

    public void Export(string path)
    {
        using var sw = new StreamWriter(path);
        sw.WriteLine("Id;StudentId;Subject;Value");
        foreach (var g in GetAll())
            sw.WriteLine($"{g.Id};{g.StudentId};{g.Subject};{g.Value}");
    }

    public void Import(string path)
    {
        foreach (var line in File.ReadAllLines(path).Skip(1))
        {
            var d = line.Split(';');
            Add(new Grade(int.Parse(d[1]), d[2], int.Parse(d[3])));
        }
    }
}