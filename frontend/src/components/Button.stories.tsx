import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '@mui/material';

const meta: Meta<typeof Button> = {
  component: Button,
  title: 'Example/Button',
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { children: 'Primary', color: 'primary', variant: 'contained' },
};

export const Secondary: Story = {
  args: { children: 'Secondary', color: 'secondary', variant: 'outlined' },
};
