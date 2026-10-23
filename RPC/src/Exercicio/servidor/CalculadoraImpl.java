package servidor;

import comum.Calculadora;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class CalculadoraImpl extends UnicastRemoteObject implements Calculadora {
    public CalculadoraImpl() throws RemoteException {
        super(1099);
    }

    @Override
    public int somar(int a, int b) throws RemoteException {
        System.out.println("Pedido de soma recebido: " + a + " + " + b);
        return a + b;
    }

    @Override
    public int subtrair(int a, int b) throws RemoteException {
        System.out.println("Pedido de subtração recebido: " + a + " - " + b);
        return a - b;
    }

    @Override
    public int multiplicar(int a, int b) throws RemoteException {
        System.out.println("Pedido de multiplicação recebido: " + a + " * " + b);
        return a * b;
    }

    @Override
    public double dividir(double a, double b) throws RemoteException {
        System.out.println("Pedido de divisão recebido: " + a + " / " + b);
        if (b == 0) {
            throw new ArithmeticException("Tentativa de divisão por zero!");
        }
        return (double) a / b;
    }
}
