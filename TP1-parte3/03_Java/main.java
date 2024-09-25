import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Main
{

  private static int semilla = 5;

  public static void main(String[] args)
  {
    Bano bano = new Bano();

    List<String> nombresHombres = new ArrayList<>(List.of("Daro", "Matias", "Esteban", "Maximo", "Mariano", "Messi", "Duki", "Diego", "Victor", "Fran", "Pato"));
    List<String> nombresMujeres = new ArrayList<>(List.of("Martu", "Ro", "Bren", "Cami", "Shakira", "Pampita", "Nicky", "Luz", "Emilia"));

    Random random = new Random();
    int cantidadEmpleados = random.nextInt(semilla) + semilla; 

    Thread[] empleados = new Thread[cantidadEmpleados];
    for (int i = 0; i < empleados.length; i++)
    {
      String genero = random.nextBoolean() ? "Hombre" : "Mujer";
      String nombre;

      if (genero.equals("Hombre") && !nombresHombres.isEmpty())
      {
        nombre = nombresHombres.remove(random.nextInt(nombresHombres.size()));
      }
      else if (genero.equals("Mujer") && !nombresMujeres.isEmpty())
      {
        nombre = nombresMujeres.remove(random.nextInt(nombresMujeres.size())); 
      }
      else
      {
        System.out.println("No hay suficientes nombres disponibles.");
        break; 
      }

      empleados[i] = new Thread(new Empleado(bano, nombre, genero));
      empleados[i].start();
    }

    for (Thread empleado : empleados)
    {
      try
      {
        empleado.join();
      }
      catch (InterruptedException e)
      {
        e.printStackTrace();
      }
    }
  }
}
