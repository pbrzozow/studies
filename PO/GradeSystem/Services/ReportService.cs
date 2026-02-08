using GradeSystem.Models;

namespace GradeSystem.Services;

public sealed class ReportService
{
    public double CalculateAverage(IEnumerable<Grade> grades, int studentId)
    {
        var selected = grades.Where(g => g.StudentId == studentId).ToList();
        return selected.Any() ? selected.Average(g => g.Value) : 0;
    }
}