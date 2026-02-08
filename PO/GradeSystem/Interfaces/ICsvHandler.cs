namespace GradeSystem.Interfaces;

public interface ICsvHandler<T>
{
    void Import(string path);
    void Export(string path);
}