#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>

const int MAX_BABOONS = 5;
const int TOTAL_BABOONS = 10;
const int LEFT_TO_RIGHT = 1;
const int RIGHT_TO_LEFT = 2;
const int MIN_CROSSING_TIME = 1;
const int MAX_CROSSING_TIME = 3;
const int DIRECTION_START_INDEX = 0;
const int DIRECTION_OFFSET = 1;
const int DIRECTION_MODIFIER = 2;
const int NO_CROSSING_BABOONS = 0;
const int OK = 0;

class Semaphore
{
  public:
    Semaphore(int count = NO_CROSSING_BABOONS) : count_(count) {}

    void acquire()
    {
      std::unique_lock<std::mutex> lock(mtx_);
      cv_.wait(lock, [this]()
        { return count_ > NO_CROSSING_BABOONS; });
      --count_;
    }

    void release()
    {
      std::unique_lock<std::mutex> lock(mtx_);
      ++count_;
      cv_.notify_one();
    }

  private:
    std::mutex mtx_;
    std::condition_variable cv_;
    int count_;
};

std::mutex mtx;
std::condition_variable cv;
Semaphore sem(MAX_BABOONS);
int crossing_baboons = 0;
int direction = 0;

std::mutex print_mtx;

void acquire_rope(int dir)
{
  std::unique_lock<std::mutex> lock(mtx);
  while (crossing_baboons > NO_CROSSING_BABOONS && direction != dir)
  {
    cv.wait(lock);
  }

  direction = dir;

  sem.acquire();

  crossing_baboons++;
}

void release_rope()
{
  std::unique_lock<std::mutex> lock(mtx);
  crossing_baboons--;
  if (crossing_baboons == NO_CROSSING_BABOONS)
  {
    direction = DIRECTION_START_INDEX;
    cv.notify_all();
  }

  sem.release();
}

void simulate_crossing(int id, int dir)
{

  std::lock_guard<std::mutex> lock(print_mtx);
  std::cout << "Babuino " << id << " está cruzando en dirección " << (dir == LEFT_TO_RIGHT ? "izquierda a derecha" : "derecha a izquierda") << std::endl;

  std::this_thread::sleep_for(std::chrono::seconds(MIN_CROSSING_TIME + rand() % MAX_CROSSING_TIME));

  std::cout << "Babuino " << id << " terminó de cruzar." << std::endl;
}

void baboon_cross(int id, int dir)
{
  acquire_rope(dir);
  simulate_crossing(id, dir);
  release_rope();
}

int main()
{
  srand(time(0));

  std::thread baboons[TOTAL_BABOONS];

  for (int i = DIRECTION_START_INDEX; i < TOTAL_BABOONS; i++)
  {
    int dir = (i % DIRECTION_MODIFIER) + DIRECTION_OFFSET;
    baboons[i] = std::thread(baboon_cross, i, dir);
  }

  for (int i = DIRECTION_START_INDEX; i < TOTAL_BABOONS; i++)
  {
    baboons[i].join();
  }

  return OK;
}