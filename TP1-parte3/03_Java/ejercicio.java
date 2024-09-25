import java.util.concurrent.Semaphore;
import java.util.LinkedList;
import java.util.Queue;

class Bano
{
  private static int NoCapacidad = 0;
  private static int InicioContadorCola = 1;
  private static int BanoVacio = 0;

  private int capacidad = 3;
  private Semaphore semaforoCapacidad = new Semaphore(capacidad, true);
  private Semaphore semaforoGenero = new Semaphore(1, true);
  private String generoEnUso = "";
  private int contadorPersonaBano = 0;
  private Queue<Empleado> colaEspera = new LinkedList<>();

  public synchronized void entrarAlBano(Empleado empleado) throws InterruptedException
  {
    String nombre = empleado.getNombre();
    String genero = empleado.getGenero();

    System.out.println(nombre + " (" + genero + ") intenta entrar al baño");

    if (!colaEspera.contains(empleado))
    {
      colaEspera.add(empleado);
      System.out.println(nombre + " (" + genero + ") ha sido agregado a la cola de espera.");
      int numero = InicioContadorCola;
      for (Empleado emp : colaEspera)
      {
        System.out.println("\t[" + numero + "| " + emp.getNombre() + " (" + emp.getGenero() + ")]");
        numero++;
      }
    }

    while ((!generoEnUso.isEmpty() && !generoEnUso.equals(genero)) || semaforoCapacidad.availablePermits() == NoCapacidad || colaEspera.peek() != empleado)
    {
      wait();
    }

    colaEspera.remove();
    System.out.println(nombre + " (" + genero + ") ha sido removido de la cola de espera.");
    int numero = InicioContadorCola;
    for (Empleado emp : colaEspera)
    {
      System.out.println("\t[" + numero + "| " + emp.getNombre() + " (" + emp.getGenero() + ")]");
      numero++;
    }

    if (generoEnUso.isEmpty())
    {
      semaforoGenero.acquire();
      generoEnUso = genero; 
      System.out.println(nombre + " (" + genero + ") ha entrado al baño. Solo puede haber " + genero + " hasta que salga.");
    }

    semaforoCapacidad.acquire();
    contadorPersonaBano++; 
    System.out.println(nombre + " (" + genero + ") ha entrado al baño. Espacios restantes: " + semaforoCapacidad.availablePermits());
  }

  public synchronized void salirDelBano(String nombre, String genero)
  {
    semaforoCapacidad.release();
    contadorPersonaBano--; 
    System.out.println(nombre + " (" + genero + ") ha salido del baño. Espacios restantes: " + semaforoCapacidad.availablePermits());

    if (contadorPersonaBano == BanoVacio)
    {
      generoEnUso = ""; 
      System.out.println("El baño está vacío. No hay nadie más en el baño. Ya se puede cambiar de género.");
      semaforoGenero.release(); 
    }

    notifyAll();
  }
}

class Empleado implements Runnable
{

  private static int tiempoEnBano = 1000;

  private Bano bano;
  private String nombre;
  private String genero;

  public Empleado(Bano bano, String nombre, String genero)
  {
    this.bano = bano;
    this.nombre = nombre;
    this.genero = genero;
  }

  public String getNombre()
  {
    return nombre;
  }

  public String getGenero()
  {
    return genero;
  }

  @Override
  public void run()
  {
    try
    {
      bano.entrarAlBano(this);
      Thread.sleep((int) (Math.random() * tiempoEnBano));
      bano.salirDelBano(nombre, genero);
    }
    catch (InterruptedException e)
    {
      e.printStackTrace();
    }
  }
}