import { useEffect, useRef, useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const GRID_SIZE = 20;
const CELL_SIZE = 20;
const INITIAL_SNAKE = [{ x: 10, y: 10 }];
const INITIAL_DIRECTION = { x: 1, y: 0 };
const GAME_SPEED = 150;

type Position = { x: number; y: number };
type Direction = { x: number; y: number };
type MushroomType = "small" | "medium" | "large";
type Mushroom = { position: Position; type: MushroomType };
type SnakeSegment = Position & { width: number };

const MUSHROOM_TYPES: { type: MushroomType; emoji: string; width: number; points: number }[] = [
  { type: "small", emoji: "🍄", width: 1, points: 10 },
  { type: "medium", emoji: "🟫", width: 1.3, points: 20 },
  { type: "large", emoji: "🍁", width: 1.6, points: 30 },
];

export const WormGame = () => {
  const [snake, setSnake] = useState<SnakeSegment[]>([{ ...INITIAL_SNAKE[0], width: 1 }]);
  const [direction, setDirection] = useState<Direction>(INITIAL_DIRECTION);
  const [mushroom, setMushroom] = useState<Mushroom>({ 
    position: { x: 15, y: 15 }, 
    type: "small" 
  });
  const [isGameOver, setIsGameOver] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [score, setScore] = useState(0);
  const directionRef = useRef<Direction>(INITIAL_DIRECTION);
  const gameLoopRef = useRef<number>();

  const generateMushroom = useCallback((snakeBody: SnakeSegment[]): Mushroom => {
    let newPosition: Position;
    do {
      newPosition = {
        x: Math.floor(Math.random() * GRID_SIZE),
        y: Math.floor(Math.random() * GRID_SIZE),
      };
    } while (snakeBody.some((segment) => segment.x === newPosition.x && segment.y === newPosition.y));
    
    const randomType = MUSHROOM_TYPES[Math.floor(Math.random() * MUSHROOM_TYPES.length)];
    return { position: newPosition, type: randomType.type };
  }, []);

  const resetGame = () => {
    setSnake([{ ...INITIAL_SNAKE[0], width: 1 }]);
    setDirection(INITIAL_DIRECTION);
    directionRef.current = INITIAL_DIRECTION;
    setMushroom({ position: { x: 15, y: 15 }, type: "small" });
    setIsGameOver(false);
    setIsPlaying(false);
    setScore(0);
  };

  const startGame = () => {
    resetGame();
    setIsPlaying(true);
  };

  const checkCollision = useCallback((head: Position, body: Position[]) => {
    // Check wall collision
    if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
      return true;
    }
    // Check self collision
    return body.some((segment) => segment.x === head.x && segment.y === head.y);
  }, []);

  const gameLoop = useCallback(() => {
    setSnake((prevSnake) => {
      const head = prevSnake[0];
      const newHead: SnakeSegment = {
        x: head.x + directionRef.current.x,
        y: head.y + directionRef.current.y,
        width: head.width,
      };

      if (checkCollision(newHead, prevSnake.slice(1))) {
        setIsGameOver(true);
        setIsPlaying(false);
        return prevSnake;
      }

      const newSnake = [newHead, ...prevSnake];

      // Check if mushroom is eaten
      if (newHead.x === mushroom.position.x && newHead.y === mushroom.position.y) {
        const mushroomData = MUSHROOM_TYPES.find(m => m.type === mushroom.type)!;
        setScore((prev) => prev + mushroomData.points);
        
        // Increase width of all segments
        const widenedSnake = newSnake.map(segment => ({
          ...segment,
          width: Math.min(segment.width * mushroomData.width, 2.5), // Max width cap
        }));
        
        setMushroom(generateMushroom(widenedSnake));
        return widenedSnake;
      } else {
        newSnake.pop();
      }

      return newSnake;
    });
  }, [mushroom, checkCollision, generateMushroom]);

  useEffect(() => {
    if (isPlaying && !isGameOver) {
      gameLoopRef.current = window.setInterval(gameLoop, GAME_SPEED);
      return () => {
        if (gameLoopRef.current) clearInterval(gameLoopRef.current);
      };
    }
  }, [isPlaying, isGameOver, gameLoop]);

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (!isPlaying || isGameOver) return;

      const key = e.key;
      const currentDir = directionRef.current;

      if (key === "ArrowUp" && currentDir.y === 0) {
        directionRef.current = { x: 0, y: -1 };
        setDirection({ x: 0, y: -1 });
      } else if (key === "ArrowDown" && currentDir.y === 0) {
        directionRef.current = { x: 0, y: 1 };
        setDirection({ x: 0, y: 1 });
      } else if (key === "ArrowLeft" && currentDir.x === 0) {
        directionRef.current = { x: -1, y: 0 };
        setDirection({ x: -1, y: 0 });
      } else if (key === "ArrowRight" && currentDir.x === 0) {
        directionRef.current = { x: 1, y: 0 };
        setDirection({ x: 1, y: 0 });
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [isPlaying, isGameOver]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen gap-6 p-4">
      <div className="text-center space-y-2">
        <h1 className="text-5xl font-bold tracking-tight" style={{ fontFamily: "monospace" }}>
          WORM GAME
        </h1>
        <p className="text-muted-foreground text-lg">Use arrow keys to control the worm</p>
      </div>

      <Card className="p-6 bg-card border-game-border shadow-2xl">
        <div className="mb-4 flex justify-between items-center">
          <div
            className="text-2xl font-bold tracking-wider"
            style={{ fontFamily: "monospace" }}
          >
            SCORE: {score}
          </div>
          {!isPlaying && !isGameOver && (
            <Button onClick={startGame} variant="default" size="lg">
              START GAME
            </Button>
          )}
          {isGameOver && (
            <Button onClick={startGame} variant="destructive" size="lg">
              RESTART
            </Button>
          )}
        </div>

        <div
          className="relative bg-game-grid rounded-lg"
          style={{
            width: GRID_SIZE * CELL_SIZE,
            height: GRID_SIZE * CELL_SIZE,
            border: "3px solid hsl(var(--game-border))",
            boxShadow: "0 0 30px rgba(34, 197, 94, 0.3)",
          }}
        >
          {/* Grid lines */}
          {Array.from({ length: GRID_SIZE }).map((_, i) => (
            <div key={`v-${i}`}>
              <div
                className="absolute bg-border/10"
                style={{
                  left: i * CELL_SIZE,
                  top: 0,
                  width: 1,
                  height: GRID_SIZE * CELL_SIZE,
                }}
              />
              <div
                className="absolute bg-border/10"
                style={{
                  left: 0,
                  top: i * CELL_SIZE,
                  width: GRID_SIZE * CELL_SIZE,
                  height: 1,
                }}
              />
            </div>
          ))}

          {/* Snake */}
          {snake.map((segment, index) => {
            const segmentSize = (CELL_SIZE - 4) * segment.width;
            const offset = (CELL_SIZE - segmentSize) / 2;
            return (
              <div
                key={`snake-${index}`}
                className="absolute rounded-sm transition-all duration-75"
                style={{
                  left: segment.x * CELL_SIZE + offset,
                  top: segment.y * CELL_SIZE + offset,
                  width: segmentSize,
                  height: segmentSize,
                  backgroundColor: "hsl(var(--game-worm))",
                  boxShadow:
                    index === 0
                      ? "0 0 15px hsl(var(--game-worm-glow))"
                      : "0 0 8px hsl(var(--game-worm-glow))",
                }}
              />
            );
          })}

          {/* Mushroom */}
          <div
            className="absolute animate-pulse flex items-center justify-center"
            style={{
              left: mushroom.position.x * CELL_SIZE,
              top: mushroom.position.y * CELL_SIZE,
              width: CELL_SIZE,
              height: CELL_SIZE,
              fontSize: CELL_SIZE - 2,
              filter: "drop-shadow(0 0 8px hsl(var(--game-food-glow)))",
            }}
          >
            {MUSHROOM_TYPES.find(m => m.type === mushroom.type)?.emoji}
          </div>

          {/* Game Over Overlay */}
          {isGameOver && (
            <div className="absolute inset-0 bg-background/90 flex items-center justify-center rounded-lg">
              <div className="text-center space-y-2">
                <h2
                  className="text-4xl font-bold text-destructive"
                  style={{ fontFamily: "monospace" }}
                >
                  GAME OVER
                </h2>
                <p className="text-xl text-foreground" style={{ fontFamily: "monospace" }}>
                  Final Score: {score}
                </p>
              </div>
            </div>
          )}

          {/* Start Overlay */}
          {!isPlaying && !isGameOver && (
            <div className="absolute inset-0 bg-background/80 flex items-center justify-center rounded-lg">
              <div className="text-center space-y-4">
                <p
                  className="text-2xl text-primary animate-pulse"
                  style={{ fontFamily: "monospace" }}
                >
                  Press START to Play
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="mt-4 text-sm text-muted-foreground text-center space-y-1">
          <p>↑ ↓ ← → Arrow keys to move</p>
          <p>🍄 Small (+10pts, +width) | 🟫 Medium (+20pts, ++width) | 🍁 Large (+30pts, +++width)</p>
        </div>
      </Card>
    </div>
  );
};
