// Copyright (c) 2024 Ole-Christoffer Granmo

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef BOARD_DIM
    #define BOARD_DIM 7
#endif

#ifndef CLASS_DATASET_SIZE
	#define CLASS_DATASET_SIZE 5000 // Total dataset is double
#endif

int neighbors[] = {-(BOARD_DIM+2) + 1, -(BOARD_DIM+2), -1, 1, (BOARD_DIM+2), (BOARD_DIM+2) - 1};

struct hex_game {
	int board[(BOARD_DIM+2)*(BOARD_DIM+2)*2];
	int open_positions[BOARD_DIM*BOARD_DIM];
	int number_of_open_positions;
	int moves[BOARD_DIM*BOARD_DIM];
	int connected[(BOARD_DIM+2)*(BOARD_DIM+2)*2];
};

void hg_init(struct hex_game *hg)
{
	const int stride = BOARD_DIM + 2;

	// Clear board + connectivity
	for (int i = 0; i < stride * stride; ++i) {
		hg->board[i * 2]     = 0;
		hg->board[i * 2 + 1] = 0;
		hg->connected[i * 2]     = 0;
		hg->connected[i * 2 + 1] = 0;
	}

	// Initialize open positions (playable cells only)
	int idx = 0;
	for (int i = 1; i <= BOARD_DIM; ++i) {
		for (int j = 1; j <= BOARD_DIM; ++j) {
			hg->open_positions[idx++] = i * stride + j;
		}
	}

	hg->number_of_open_positions = BOARD_DIM * BOARD_DIM;
}

int hg_connect(struct hex_game *hg, int player, int position)
{
	// Terminal edge reached
	if (player == 0 && position / (BOARD_DIM + 2) == BOARD_DIM + 1)
		return 1;

	if (player == 1 && position % (BOARD_DIM + 2) == BOARD_DIM + 1)
		return 1;

	hg->connected[position*2 + player] = 1;

	for (int i = 0; i < 6; ++i) {
		int neighbor = position + neighbors[i];

		// If neighbor is terminal padding → win
		if (player == 0 && neighbor / (BOARD_DIM + 2) == BOARD_DIM + 1)
			return 1;

		if (player == 1 && neighbor % (BOARD_DIM + 2) == BOARD_DIM + 1)
			return 1;

		// Continue DFS through stones only
		if (hg->board[neighbor*2 + player] &&
			!hg->connected[neighbor*2 + player]) {
			if (hg_connect(hg, player, neighbor))
				return 1;
			}
	}

	return 0;
}

int hg_winner(struct hex_game *hg, int player, int position)
{
	int row = position / (BOARD_DIM + 2);
	int col = position % (BOARD_DIM + 2);

	// Player 0 (X): top → bottom
	if (player == 0) {
		if (row != 1) return 0;
	}
	// Player 1 (O): left → right
	else {
		if (col != 1) return 0;
	}

	return hg_connect(hg, player, position);
}


int hg_place_piece_randomly(struct hex_game *hg, int player)
{
	int random_empty_position_index = rand() % hg->number_of_open_positions;

	int empty_position = hg->open_positions[random_empty_position_index];

	hg->board[empty_position * 2 + player] = 1;

	hg->moves[BOARD_DIM*BOARD_DIM - hg->number_of_open_positions] = empty_position;

	hg->open_positions[random_empty_position_index] = hg->open_positions[hg->number_of_open_positions-1];

	hg->number_of_open_positions--;

	return empty_position;
}

int hg_full_board(struct hex_game *hg)
{
	return hg->number_of_open_positions == 0;
}

void hg_print(struct hex_game *hg)
{
	for (int i = 0; i < BOARD_DIM; ++i) {
		for (int j = 0; j < i; j++) {
			printf(" ");
		}

		for (int j = 0; j < BOARD_DIM; ++j) {
			if (hg->board[((i+1)*(BOARD_DIM+2) + j + 1)*2] == 1) {
				printf(" X");
			} else if (hg->board[((i+1)*(BOARD_DIM+2) + j + 1)*2 + 1] == 1) {
				printf(" 0");
			} else {
				printf(" .");
			}
		}
		printf("\n");
	}
}

void add_char_to_string(char *s, char c)
{
	size_t l = strlen(s);
	s[l] = c;
	s[l+1] = '\0';
}

void file_wipe()
{
	char dataset_fpath[30];
	sprintf(dataset_fpath, "games/%d/%d.txt", BOARD_DIM, 0);

	FILE *fptr = fopen(dataset_fpath, "w");
	fprintf(fptr, "");
	fclose(fptr);

	sprintf(dataset_fpath, "games/%d/%d.txt", BOARD_DIM, 1);
	fptr = fopen(dataset_fpath, "w");
	fprintf(fptr, "");
	fclose(fptr);
}

void hg_file_write(struct hex_game *hg, int winner)
{
	char dataset_fpath[30];
	sprintf(dataset_fpath, "games/%d/%d.txt", BOARD_DIM, winner);

	FILE *fptr = fopen(dataset_fpath, "a");

	char hg_str[BOARD_DIM * BOARD_DIM + 10] = "";

	for (int i = 0; i < BOARD_DIM; ++i)
	{
		for (int j = 0; j < BOARD_DIM; ++j)
		{
			if (hg->board[((i+1)*(BOARD_DIM+2) + j + 1)*2] == 1)
			{
				add_char_to_string(hg_str, 'X');
			}
			else if (hg->board[((i+1)*(BOARD_DIM+2) + j + 1)*2 + 1] == 1)
			{
				add_char_to_string(hg_str, '0');
			}
			else
			{
				add_char_to_string(hg_str, '.');
			}
		}
	}
	add_char_to_string(hg_str, '\n');

	fprintf(fptr, "%s", hg_str);

	fclose(fptr);
}

int main()
{
	struct hex_game hg;

	int winner = -1;

	int valid_0_wins = 0;
	int valid_1_wins = 0;

	file_wipe();

	while (valid_0_wins < CLASS_DATASET_SIZE || valid_1_wins < CLASS_DATASET_SIZE)
	{
		hg_init(&hg);

		int player = 0;
		while (!hg_full_board(&hg))
		{
			int position = hg_place_piece_randomly(&hg, player);
			
			if (hg_winner(&hg, player, position))
			{
				winner = player;
				break;
			}

			player = 1 - player;
		}

		// If open positions more than 45% of board size, validate game
		const int open_pos_req = BOARD_DIM * BOARD_DIM * 0.45;
		// const int open_pos_req = 0;

		if (hg.number_of_open_positions >= open_pos_req)
		{
			printf("\nPlayer %d wins!\n", winner);

			if (winner == 0 && valid_0_wins < CLASS_DATASET_SIZE)
			{
				valid_0_wins++;
				hg_file_write(&hg, winner);
			}
			else if (winner == 1 && valid_1_wins < CLASS_DATASET_SIZE)
			{
				valid_1_wins++;
				hg_file_write(&hg, winner);
			}

			if (valid_0_wins + valid_1_wins % 100)
				printf("Progress: %d / %d\n", valid_0_wins + valid_1_wins, CLASS_DATASET_SIZE * 2);
		}
	}

	printf("\nPlayer 0: %c (Bot-Top) -- %d wins\n", 'X', valid_0_wins);
	printf("Player 1: %c (Left-Right) -- %d wins\n", '0', valid_1_wins);
}