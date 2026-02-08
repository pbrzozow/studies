namespace GradeSystem.Models;

public sealed class Grade
{
    public int Id { get; set; }
    public int StudentId { get; }
    public string Subject { get; }
    public int Value { get; private set; }

    public Grade(int studentId, string subject, int value)
    {
        if (value < 2 || value > 5)
            throw new ArgumentException("Ocena musi być w zakresie 2–5");

        StudentId = studentId;
        Subject = subject;
        Value = value;
    }

    public void ChangeValue(int newValue)
    {
        if (newValue < 2 || newValue > 5)
            throw new ArgumentException("Ocena musi być w zakresie 2–5");
        Value = newValue;
    }
}