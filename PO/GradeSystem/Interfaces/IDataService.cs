namespace GradeSystem.Interfaces;

public interface IDataService<T>
{
    void Add(T item);
    void Update(T item);
    void Delete(int id);
    List<T> GetAll();
}